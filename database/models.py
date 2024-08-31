from sqlalchemy import create_engine, Column, Integer, String, Boolean, Table
import sqlalchemy
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./backend.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# association table for the many-to-many relationship between users and tasks
user_tasks = Table(
    "user_tasks",
    Base.metadata,
    Column("user_id", Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True),
    Column("task_id", Integer, sqlalchemy.ForeignKey("tasks.id"), primary_key=True)
)


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    tasks_done = relationship("TaskEntity", secondary=user_tasks, back_populates="doneBy")

    @staticmethod
    def get_user(db, username: str):
        return db.query(UserEntity).filter(UserEntity.username == username).first()


class TaskEntity(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    isCompleted = Column(Boolean)
    assignedUsers = Column(String)
    doneBy = relationship("UserEntity", secondary=user_tasks, back_populates="tasks_done")
    author = Column(String)
    timestamp = Column(Integer)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def model_dump(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "isCompleted": self.isCompleted,
            "assignedUsers": self.assignedUsers,
            "doneBy": [user.username for user in self.doneBy],
            "author": self.author,
            "timestamp": self.timestamp
        }


Base.metadata.create_all(bind=engine)
