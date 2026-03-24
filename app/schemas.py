from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True

#                                                                      Таски
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    project_id: int
    assignee_id: Optional[int] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True