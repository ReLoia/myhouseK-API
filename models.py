from pydantic import BaseModel


class CreateTaskModel(BaseModel):
    title: str
    description: str
    assignedUsers: str


class EditTaskModel(BaseModel):
    id: int
    title: str
    description: str
    assignedUsers: str


class UserModel(BaseModel):
    username: str
    tasks_done: list[str]


class TaskModel(BaseModel):
    id: int
    title: str
    description: str
    isCompleted: bool
    assignedUsers: str
    doneBy: list[UserModel]
    author: str
    timestamp: int


class UserRegisterModel(BaseModel):
    username: str
    password: str


class Message(BaseModel):
    message: str
