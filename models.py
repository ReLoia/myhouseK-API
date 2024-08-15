from pydantic import BaseModel


class TaskModel(BaseModel):
    title: str
    description: str
    isCompleted: bool
    assignedUsers: list[str]
    timestamp: int
    author: str
