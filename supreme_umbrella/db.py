import os
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


def init_db() -> None:
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        cur = db.cursor()
        cur.execute(f.read())


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    init_db()
    click.echo("Initialized the database.")


def init_app(app: "Flask") -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
