from ninja import Schema
from pydantic import EmailStr


class PasswordlessAuthIn(Schema):
    phone_number: str


class PasswordlessAuthConfirmationIn(Schema):
    phone_number: str
    verification_code: str


class PasswordlessAccountOut(Schema):
    phone_number: str
    email: EmailStr = None
    name: str = None


class PasswordlessUpdateIn(Schema):
    email: EmailStr = None
    name: str = None


class PasswordlessAuthMessageOut(Schema):
    status: str
    message: str
    token: str = None
