import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr
    referral_code: str | None = None


class LoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class ActiveSession(BaseModel):
    email: EmailStr
    access_token: str
    expiry_time: datetime.datetime
