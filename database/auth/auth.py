# Methods for authentication
from passlib.context import CryptContext
import motor.motor_asyncio

from ..models import UserEntity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: motor.motor_asyncio.AsyncIOMotorDatabase, username: str):
    return db.query(UserEntity).filter(UserEntity.username == username).first()


def authenticate_user(db: motor.motor_asyncio.AsyncIOMotorDatabase, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
