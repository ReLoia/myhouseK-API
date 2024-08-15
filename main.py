import os
from typing import List

import motor.motor_asyncio
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from models import TaskModel
from security.index import check_api_key
from database.index import load_db
from database.models import TaskEntity

app = FastAPI()
load_dotenv()

db = load_db()
tasks_collection = db.get_collection("tasks")


@app.get("/")
async def root():
    # TODO:
    return {"message": "Hello World"}


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(
        _: None = Depends(check_api_key)
):
    print("Getting tasks")
    tasks = await tasks_collection.find().to_list(100)
    print(
        tasks
    )
    #     TODO: Get all tasks from database
    return tasks


@app.post("/tasks", response_model=TaskModel)
async def create_task(
        task: TaskModel,
        _: None = Depends(check_api_key)
):
    print("Creating task")
    new_task = await tasks_collection.insert_one(task.model_dump())
    created_task = await tasks_collection.find_one({"_id": new_task.inserted_id})

    return TaskModel(**created_task)
