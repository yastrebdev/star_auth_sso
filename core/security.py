from datetime import timedelta, datetime, timezone
from pathlib import Path

import jwt
from passlib.context import CryptContext
from config import settings

####################
# PASSWORD HASHING #
####################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


####################
# WORKING WITH JWT #
####################

private_key: str = Path(settings.auth_jwt.private_key_path).read_text(encoding="utf-8")
public_key: str = Path(settings.auth_jwt.public_key_path).read_text(encoding="utf-8")


def encode_jwt(
    payload: dict,
    private_key: str = private_key,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp = expire,
        iat = now
    )
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = public_key,
    algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded