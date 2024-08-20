from pydantic import BaseModel


class TaskModel(BaseModel):
    """
    TaskModel is the Pydantic model of the data that is sent from the server to the client.
    """
    id: str
    title: str
    description: str
    isCompleted: bool
    assignedUsers: str
    author: str
    timestamp: int


class CreateTaskModel(BaseModel):
    """
    TaskModel is the Pydantic model that will be used to validate the data that is sent to the server when creating a
    new task or editing an existing one.
    """
    title: str
    description: str
    assignedUsers: str


class UserModel(BaseModel):
    username: str
    tasks_done: list[str]


class UserRegisterModel(BaseModel):
    username: str
    password: str


class Message(BaseModel):
    message: str
