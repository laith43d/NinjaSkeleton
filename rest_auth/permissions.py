import datetime
from typing import Optional, Any

from django.conf import settings
from django.http import HttpRequest
from jose import jwt, JWTError
from ninja.security import HttpBearer

from rest_auth.models import PasswordlessAccount, EmailAccount

TIME_DELTA = datetime.timedelta(days=30)


def decode_token(token):
    return jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=['HS256'])


def encode_token(user, user_type: str = 'PU'):
    if user_type == "PU":
        return jwt.encode(claims={'user': user.phone_number, 'exp': datetime.datetime.utcnow() + TIME_DELTA},
                          key=settings.SECRET_KEY,
                          algorithm='HS256')
    return jwt.encode(claims={'user': str(user.id), 'exp': datetime.datetime.utcnow() + TIME_DELTA},
                      key=settings.SECRET_KEY,
                      algorithm='HS256')


class PasswordlessAuthorization(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        try:
            user_pk = decode_token(token)
        except JWTError as e:
            return e

        user = PasswordlessAccount.objects.get(phone_number=user_pk['user'])
        if user:
            return {'user': user, 'token': token}


class EmailAuthorization(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        try:
            user_pk = decode_token(token)

        except JWTError as e:
            return e

        user = EmailAccount.objects.get(id=user_pk['user'])
        if user:
            return {'user': user, 'token': token}


def get_token_for_user(user, user_type: str):
    token = encode_token(user, user_type)
    return str(token)
