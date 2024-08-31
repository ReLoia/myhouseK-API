import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.auth.auth import verify_password, get_password_hash
from database.auth.security import create_access_token, get_user_from_token, validate_object_id
from database.session import get_db
from database.models import UserEntity, TaskEntity

from models import TaskModel, UserModel, CreateTaskModel, Message
from utils import TODO

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
        db: Session = Depends(get_db),
        _: None = Depends(get_user_from_token)
):
    # NEW CODE usign sqlalchemy and sqlite
    tasks = db.query(TaskEntity).all()
    return tasks

    # OLD CODE
    # tasks_collection = db.get_collection("tasks")
    # tasks = await tasks_collection.find().to_list(100)
    #
    # tasks = map(lambda task: {
    #     **task,
    #     "id": str(task["_id"]),
    # }, tasks)
    #
    # return tasks


@app.post("/tasks", response_model=TaskModel)
async def create_task(
        task: CreateTaskModel,
        db: Session = Depends(get_db),
        user: UserEntity = Depends(get_user_from_token)
):
    TODO()
    # OLD CODE
    # tasks_collection = db.get_collection("tasks")
    # new_task = await tasks_collection.insert_one(
    #     {
    #         **task.model_dump(),
    #         "isCompleted": False,
    #         "author": user.username,
    #         "timestamp": int(datetime.now().timestamp())
    #     })
    # created_task = await tasks_collection.find_one({"_id": new_task.inserted_id})
    #
    # return {
    #     **created_task,
    #     "id": str(created_task["_id"])
    # }


@app.put("/tasks/{task_id}", response_model=TaskModel, responses={
    404: {"description": "Task not found", "model": Message},
    400: {"description": "Invalid task ID", "model": Message}
})
async def update_task(
        task_id: str = Depends(validate_object_id),
        db: Session = Depends(get_db),
        _: None = Depends(get_user_from_token)
):
    TODO()
    # OLD CODE
    # tasks_collection = db.get_collection("tasks")
    # task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    # if not task:
    #     raise HTTPException(status_code=404, detail="Task not found")
    #
    # await tasks_collection.update_one({"_id": task_id}, {"$set": task.model_dump()})
    #
    # updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    #
    # return {
    #     **updated_task,
    #     "id": str(updated_task["_id"])
    # }


@app.post("/tasks/{task_id}/toggle",
          response_model=Message,
          responses={
              404: {"description": "Task not found", "model": Message},
              400: {"description": "Invalid task ID", "model": Message}
          }
          )
async def toggle_task(
        task_id: str = Depends(validate_object_id),
        db: Session = Depends(get_db),
        user: UserEntity = Depends(get_user_from_token)
):
    TODO()
    # OLD CODE
    # tasks_collection = db.get_collection("tasks")
    # task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    # if not task:
    #     raise HTTPException(status_code=404, detail="Task not found")
    #
    # await tasks_collection.update_one({"_id": task_id}, {"$set": {"isCompleted": not task["isCompleted"]}})
    #
    # return {"message": "Task updated"}


@app.delete("/tasks/{task_id}",
            response_model=Message,
            responses={
                404: {"description": "Task not found", "model": Message},
                400: {"description": "Invalid task ID", "model": Message}
            }
            )
async def delete_task(
        task_id: str = Depends(validate_object_id),
        db: Session = Depends(get_db),
        _: None = Depends(get_user_from_token)
):
    TODO()
    # OLD CODE
    # tasks_collection = db.get_collection("tasks")
    # task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    # if not task:
    #     raise HTTPException(status_code=404, detail="Task not found")
    #
    # await tasks_collection.delete_one({"_id": task_id})
    #
    # return {"message": "Task deleted"}


# Users API
@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    # NEW CODE
    user = db.query(UserEntity).filter(UserEntity.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


    # OLD CODE
    # user = await UserEntity.get_user(db, form_data.username)
    # if not user:
    #     return {"error": "User not found"}
    # if not verify_password(form_data.password, user.password_hash):
    #     return {"error": "Incorrect password"}
    #
    # access_token = create_access_token(data={"sub": user.username})
    #
    # return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    # NEW CODE
    user = db.query(UserEntity).filter(UserEntity.username == form_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserEntity(username=form_data.username, password_hash=get_password_hash(form_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


    # OLD CODE
    # TODO()
    # user = await UserEntity.get_user(db, form_data.username)
    # if user:
    #     return {"error": "User already exists"}
    #
    # new_user = UserEntity(username=form_data.username, password_hash=get_password_hash(form_data.password))
    #
    # result = await db.get_collection("users").insert_one(new_user.model_dump())
    # if not result.acknowledged:
    #     return {"error": "Error creating user"}
    #
    # access_token = create_access_token(data={"sub": new_user.username})
    #
    # return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=UserModel)
async def get_user(
        user: UserEntity = Depends(get_user_from_token)
):
    return user
