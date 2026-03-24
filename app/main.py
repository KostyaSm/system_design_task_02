from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List

from app.schemas import (
    UserCreate, UserResponse, UserLogin, Token,
    ProjectCreate, ProjectResponse,
    TaskCreate, TaskResponse
)
from app.models import User
from app.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, TokenData, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.database import db

app = FastAPI(
    title="Project Management API",
    description="REST API для управления проектами, задачами и исполнителями",
    version="1.0.0"
)


@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
          tags=["Authentication"])
async def register(user_data: UserCreate):

    existing_user = db.get_user_by_login(user_data.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists"
        )

    user = db.create_user(
        login=user_data.login,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    return user


@app.post("/api/auth/login", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user_by_login(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.login},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# User
@app.get("/api/users/search", response_model=UserResponse, tags=["Users"])
async def search_user_by_login(login: str):
    user = db.get_user_by_login(login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@app.get("/api/users/searchByName", response_model=List[UserResponse], tags=["Users"])
async def search_user_by_name(pattern: str):
    users = db.search_users_by_name(pattern)
    return users


# Project
@app.post("/api/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, tags=["Projects"])
async def create_project(project_data: ProjectCreate, current_user: TokenData = Depends(get_current_user)):
    creator = db.get_user_by_login(current_user.login)
    project = db.create_project(
        name=project_data.name,
        description=project_data.description,
        created_by=creator.id
    )
    return project


@app.get("/api/projects/search", response_model=List[ProjectResponse], tags=["Projects"])
async def search_project_by_name(name: str):
    projects = db.search_projects_by_name(name)
    return projects


@app.get("/api/projects", response_model=List[ProjectResponse], tags=["Projects"])
async def get_all_projects():
    return db.get_all_projects()


# task
@app.post("/api/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED,
          tags=["Tasks"])
async def create_task(project_id: int, task_data: TaskCreate, current_user: TokenData = Depends(get_current_user)):

    project = db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    task = db.create_task(
        title=task_data.title,
        project_id=project_id,
        description=task_data.description,
        assignee_id=task_data.assignee_id
    )
    return task


@app.get("/api/projects/{project_id}/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def get_project_tasks(project_id: int):
    project = db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db.get_tasks_by_project(project_id)


@app.get("/api/tasks/{task_code}", response_model=TaskResponse, tags=["Tasks"])
async def get_task_by_code(task_code: str):
    task = db.get_task_by_code(task_code)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


#Health chek
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}