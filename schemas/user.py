import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class BaseUserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(BaseUserCreate):
    password: str = Field(..., min_length=8, max_length=64)

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return value


class UserSaveDB(BaseUserCreate):
    hashed_password: str


class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: str
    first_name: str | None
    last_name: str | None
    is_active: bool

    class Config:
        orm_mode = True