import os
from datetime import datetime
from typing import List

import motor.motor_asyncio
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database.auth.auth import verify_password, get_password_hash
from database.auth.security import create_access_token, get_user_from_token
# from security.index import check_api_key
from database.index import get_db
from database.models import TaskEntity, UserEntity
from utils import TODO
# models for FastAPI
from models import TaskModel, UserModel, UserRegisterModel, CreateTaskModel

app = FastAPI(
    title="MyHouseK API",
    description="API for MyHouseK application",
    version="0.1.0"
)
load_dotenv()
# security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# Tasks API
@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db),
        _: None = Depends(get_user_from_token)
):
    tasks_collection = db.get_collection("tasks")
    tasks = await tasks_collection.find().to_list(100)

    return tasks


@app.post("/tasks", response_model=TaskModel)
async def create_task(
        task: CreateTaskModel,
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db),
        user: UserEntity = Depends(get_user_from_token)
):
    tasks_collection = db.get_collection("tasks")
    new_task = await tasks_collection.insert_one(
        {
            **task.model_dump(),
            "author": user.username,
            "timestamp": int(datetime.now().timestamp())
        })
    created_task = await tasks_collection.find_one({"_id": new_task.inserted_id})

    return created_task


# Users API
@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    user = await UserEntity.get_user(db, form_data.username)
    if not user:
        return {"error": "User not found"}
    if not verify_password(form_data.password, user.password_hash):
        return {"error": "Incorrect password"}

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: motor.motor_asyncio.AsyncIOMotorDatabase = Depends(get_db)
):
    TODO()
    user = await UserEntity.get_user(db, form_data.username)
    if user:
        return {"error": "User already exists"}

    new_user = UserEntity(username=form_data.username, password_hash=get_password_hash(form_data.password))

    result = await db.get_collection("users").insert_one(new_user.model_dump())
    if not result.acknowledged:
        return {"error": "Error creating user"}

    access_token = create_access_token(data={"sub": new_user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user", response_model=UserModel)
async def get_user(
        user: UserEntity = Depends(get_user_from_token)
):
    return user
