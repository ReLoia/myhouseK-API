from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
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


class UserEntity(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    password_hash: str
    tasks_done: list[PyObjectId] = Field(default_factory=list)

    @staticmethod
    async def get_user(db, username) -> 'UserEntity':
        return UserEntity(**(await db["users"].find_one({"username": username})))
