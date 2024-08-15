import os
from typing import Mapping, Any

import motor.motor_asyncio

client: motor.motor_asyncio.AsyncIOMotorClient[Mapping[str, Any]] = None


def connect_db():
    global client
    if client is None:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}/test?retryWrites=true&w=majority&appName=myhousek-db"
        )


def load_db():
    global client
    connect_db()
    return client.get_database("myhousek")
