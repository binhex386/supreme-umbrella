import binascii
import os
import random
import typing

import click
import mysql.connector
from flask import current_app, g
from flask.cli import with_appcontext

if typing.TYPE_CHECKING:
    from flask import Flask
    from mysql.connector.connection import MySQLConnection


def get_db() -> "MySQLConnection":
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )
    return g.db


def close_db(ex: typing.Optional[BaseException]) -> None:
    db: "MySQLConnection" = g.pop("db", None)
    if db is not None:
        db.close()


def _load_resource(path: str) -> str:
    with current_app.open_resource(path) as f:
        return f.read()


def init_db() -> None:
    db = get_db()
    schema_sql = _load_resource("schema.sql")
    cur = db.cursor()
    cur.execute(schema_sql)


def fill_db(target_count: int, batch_size: int) -> None:
    firsts = _load_resource("names/male.txt").splitlines()
    firsts += _load_resource("names/female.txt").splitlines()
    lasts = _load_resource("names/last.txt").splitlines()
    cities = _load_resource("names/city.txt").splitlines()

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(1) FROM user")
    count: int = cur.fetchone()[0]
    click.echo(f"Got {count} of {target_count} users in the database.")

    for _ in range((target_count - count) // batch_size):
        this_batch_size = min(batch_size, target_count - count)
        for _ in range(this_batch_size):
            nick = binascii.hexlify(random.randbytes(8)).decode()
            cur.execute(
                """
                    INSERT INTO user (
                        email,
                        password_hash,
                        first_name,
                        last_name,
                        age_years,
                        interests,
                        city
                    ) VALUES (
                        %(email)s,
                        '!',
                        %(first_name)s,
                        %(last_name)s,
                        %(age_years)s,
                        'highload',
                        %(city)s
                    )
                """,
                {
                    "email": f"{nick}@example.test",
                    "first_name": random.choice(firsts),  # noqa: S311
                    "last_name": random.choice(lasts),  # noqa: S311
                    "age_years": random.randint(18, 99),
                    "city": random.choice(cities),  # noqa: S311
                },
            )
        db.commit()
        click.echo(f"Added {this_batch_size} more users.")

    cur.close()


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    init_db()
    click.echo("Initialized the database.")


@click.command("fill-db")
@click.option("--target-count", "-c", default=1_000_000)
@click.option("--batch-size", "-b", default=10_000)
@with_appcontext
def fill_db_command(target_count: int, batch_size: int) -> None:
    fill_db(target_count, batch_size)
    click.echo("Filled the database.")


def init_app(app: "Flask") -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(fill_db_command)
