from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

from database.auth.security import decode_access_token


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)


class TaskEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    isCompleted: bool
    assignedUsers: list[str]
    timestamp: int
    author: str

    @staticmethod
    def otd(obj: dict) -> 'TaskEntity':
        """
        Api Object To Database Object
        :param obj: dict
        :return: TaskEntity
        """
        return TaskEntity(**obj)


class UserEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    password_hash: str
    tasks_done: list[PyObjectId] = Field(default_factory=list)

    @staticmethod
    def get_user(db, username):
        return db["users"].find_one({"username": username})

    @staticmethod
    def get_user_by_token(db, token):
        decoded_token = decode_access_token(token)
        return db["users"].find_one({"username": decoded_token["sub"]})
