from pydantic import BaseModel


class TaskModel(BaseModel):
    title: str
    description: str
    isCompleted: bool
    assignedUsers: list[str]
    timestamp: int
    author: str


class UserModel(BaseModel):
    username: str
    tasks_done: list[str]


class UserRegisterModel(BaseModel):
    username: str
    password: str
