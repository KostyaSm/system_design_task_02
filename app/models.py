from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    password_hash: str
    first_name: str
    last_name: str
    created_at: datetime = datetime.now()


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime = datetime.now()
    created_by: int


class Task(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    project_id: int
    assignee_id: Optional[int] = None
    status: str = "OPEN"
    created_at: datetime = datetime.now()