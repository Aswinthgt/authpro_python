from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import encode
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)


def create_token(user_data: dict):
    user = user_data.copy()
    expire_date = datetime.now() + timedelta(days=1)
    if user_data:
        user.update({'exp': expire_date})
        return encode(user, os.getenv('SECRET_KEY'), os.getenv('ALGORITHM'))
    else:
        return None
