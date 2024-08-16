import os
from typing import Mapping, Any
import motor.motor_asyncio


class MongoDBClientSingleton:
    _instance = None
    _client: motor.motor_asyncio.AsyncIOMotorClient[Mapping[str, Any]] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}/test?retryWrites=true&w=majority&appName=myhousek-db"
            )

    def get_database(self, db_name: str):
        return self._client.get_database(db_name)


# Usage
def get_db():
    mongo_client = MongoDBClientSingleton()
    return mongo_client.get_database("myhousek")
