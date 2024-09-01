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

from models import TaskModel, UserModel, CreateTaskModel, Message, EditTaskModel
from utils import TODO

BASE_PATH = os.environ.get("API_ROOT_PATH", "")

app = FastAPI(
    title="MyHouseK API",
    description="API for MyHouseK application",
    version="0.2.0"
)
load_dotenv()
# security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/")
async def root():
    return RedirectResponse(url=f"{BASE_PATH}/docs")


# Tasks API
@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(
        db: Session = Depends(get_db),
        _: None = Depends(get_user_from_token)
):
    tasks = db.query(TaskEntity).all()
    return tasks


@app.post("/tasks", response_model=TaskModel)
async def create_task(
        task: CreateTaskModel,
        db: Session = Depends(get_db),
        user: UserEntity = Depends(get_user_from_token)
):
    new_task = TaskEntity(
        **task.model_dump(),
        isCompleted=False,
        author=user.username,
        timestamp=int(datetime.now().timestamp()),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.put("/tasks/", response_model=TaskModel, responses={
    404: {"description": "Task not found", "model": Message},
    400: {"description": "Invalid task ID", "model": Message}
})
async def update_task(
        task: EditTaskModel,
        db: Session = Depends(get_db),
        _: None = Depends(get_user_from_token)
):
    task = db.query(TaskEntity).filter(TaskEntity.id == task.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.update({
        "title": task.title,
        "description": task.description,
        "assignedUsers": task
    })
    db.commit()
    db.refresh(task)

    return task


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
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.isCompleted = not task.isCompleted

    db.commit()
    db.refresh(task)

    return {"message": "Task updated"}


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
    task = db.query(TaskEntity).filter(TaskEntity.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


# Users API
@app.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(UserEntity).filter(UserEntity.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(UserEntity).filter(UserEntity.username == form_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserEntity(username=form_data.username, password_hash=get_password_hash(form_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=UserModel)
async def get_user(
        user: UserEntity = Depends(get_user_from_token)
):
    return user
