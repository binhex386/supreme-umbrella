import re
import typing

from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        id: int | None,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        age_years: int,
        interests: str,
        city: str,
    ) -> None:
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.age_years = age_years
        self.interests = interests
        self.city = city

    def asdict(self) -> dict[str, typing.Any]:
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age_years": self.age_years,
            "interests": self.interests,
            "city": self.city,
        }

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def slug(self) -> str:
        return re.sub(r"[^\w]+", "-", self.display_name).lower()
