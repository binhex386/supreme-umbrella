import mysql.connector.errors

from . import db, models


class IntegrityError(Exception):
    pass


class UserRepo:
    @staticmethod
    def get_by_id(id: int) -> models.User | None:
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM user WHERE id=%s", (id,))
        data = cur.fetchone()
        cur.close()
        if not data:
            return None

        return models.User(**data)

    @staticmethod
    def get_by_email(email: str) -> models.User | None:
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM user WHERE email=%s", (email,))
        data = cur.fetchone()
        cur.close()
        if not data:
            return None

        return models.User(**data)

    @staticmethod
    def add(user: models.User) -> None:
        conn = db.get_db()
        cur = conn.cursor()
        try:
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
                        %(password_hash)s,
                        %(first_name)s,
                        %(last_name)s,
                        %(age_years)s,
                        %(interests)s,
                        %(city)s
                    )
                """,
                user.asdict(),
            )
            conn.commit()
        except mysql.connector.errors.IntegrityError:
            raise IntegrityError
        cur.close()
        user.id = cur.lastrowid

    @staticmethod
    def save(user: models.User) -> None:
        conn = db.get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                    UPDATE user SET
                        first_name=%(first_name)s,
                        last_name=%(last_name)s,
                        age_years=%(age_years)s,
                        interests=%(interests)s,
                        city=%(city)s
                    WHERE
                        id=%(id)s
                """,
                user.asdict(),
            )
            conn.commit()
        except mysql.connector.errors.IntegrityError:
            raise IntegrityError
        cur.close()

    @staticmethod
    def get_all(limit: int, offset: int) -> list[models.User]:
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM user ORDER BY id LIMIT %s OFFSET %s",
            (limit, offset),
        )
        return [models.User(**row) for row in cur]

    @staticmethod
    def search(first: str, last: str) -> list[models.User]:
        conn = db.get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
                SELECT * FROM user
                WHERE
                    first_name like %(first_name)s
                    AND last_name like %(last_name)s
                ORDER BY id
            """,
            {
                "first_name": f"{first}%",
                "last_name": f"{last}%",
            },
        )
        return [models.User(**row) for row in cur]
