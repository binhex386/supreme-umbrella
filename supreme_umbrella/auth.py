import binascii
import hashlib
import secrets

from flask_login import LoginManager

from . import models, repo

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> models.User | None:
    return repo.UserRepo.get_by_id(int(user_id))


def create_hash(
    password: str,
    hash_name: str = "sha256",
    salt_bytes: int = 32,
    iterations: int = 1_000_000,
) -> str:
    salt = secrets.token_bytes(salt_bytes)
    data = password.encode("utf8")
    hash = hashlib.pbkdf2_hmac(hash_name, data, salt, iterations)
    return "$".join(
        [
            hash_name,
            binascii.hexlify(salt).decode("ascii"),
            str(iterations),
            binascii.hexlify(hash).decode("ascii"),
        ]
    )


def verify_hash(password: str, db_hash: str) -> bool:
    hash_name, salt_str, iterations_str, hash_str = db_hash.split("$")
    salt = binascii.unhexlify(salt_str)
    iterations = int(iterations_str)
    hash = binascii.unhexlify(hash_str)
    data = password.encode("utf8")
    real_hash = hashlib.pbkdf2_hmac(hash_name, data, salt, iterations)
    return secrets.compare_digest(hash, real_hash)
