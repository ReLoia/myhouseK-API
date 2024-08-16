import os
from typing import List

import motor.motor_asyncio
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from security.index import check_api_key
from database.index import get_db
from database.models import TaskEntity, UserEntity
from utils import TODO
# models for FastAPI
from models import TaskModel, UserModel, UserRegisterModel


app = FastAPI()
load_dotenv()
# security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    #     redirect to /docs
    return RedirectResponse(url="/docs")


# Tasks API
@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db),
        _: None = Depends(oauth2_scheme)
):
    tasks_collection = db.get_collection("tasks")
    tasks = await tasks_collection.find().to_list(100)
    return tasks


@app.post("/tasks", response_model=TaskModel)
async def create_task(
        task: TaskModel,
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db),
        _: None = Depends(oauth2_scheme)
):
    tasks_collection = db.get_collection("tasks")
    new_task = await tasks_collection.insert_one(task.model_dump())
    created_task = await tasks_collection.find_one({"_id": new_task.inserted_id})

    return TaskModel(**created_task)


# Users API
@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    TODO()


@app.post("/register")
async def register():
    TODO()


@app.get("/user", response_model=UserModel)
async def get_user(
        token: str = Depends(oauth2_scheme)
):
    TODO()
