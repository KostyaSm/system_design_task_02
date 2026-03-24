from typing import Dict, List, Optional
from app.models import User, Project, Task


class InMemoryDB:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.projects: Dict[int, Project] = {}
        self.tasks: Dict[int, Task] = {}
        self.user_id_counter = 1
        self.project_id_counter = 1
        self.task_id_counter = 1
        self.task_code_counter = 1

    def create_user(self, login: str, password_hash: str, first_name: str, last_name: str) -> User:
        user = User(
            id=self.user_id_counter,
            login=login,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        self.users[self.user_id_counter] = user
        self.user_id_counter += 1
        return user

    def get_user_by_login(self, login: str) -> Optional[User]:
        for user in self.users.values():
            if user.login == login:
                return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def search_users_by_name(self, pattern: str) -> List[User]:
        result = []
        pattern_lower = pattern.lower()
        for user in self.users.values():
            full_name = f"{user.first_name} {user.last_name}".lower()
            if pattern_lower in full_name:
                result.append(user)
        return result

    # Project operattions
    def create_project(self, name: str, description: Optional[str], created_by: int) -> Project:
        project = Project(
            id=self.project_id_counter,
            name=name,
            description=description,
            created_by=created_by
        )
        self.projects[self.project_id_counter] = project
        self.project_id_counter += 1
        return project

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.projects.get(project_id)

    def search_projects_by_name(self, name: str) -> List[Project]:
        result = []
        name_lower = name.lower()
        for project in self.projects.values():
            if name_lower in project.name.lower():
                result.append(project)
        return result

    def get_all_projects(self) -> List[Project]:
        return list(self.projects.values())

    # Task
    def create_task(self, title: str, project_id: int, description: Optional[str] = None, assignee_id: Optional[int] = None) -> Task:
        task_code = f"TASK-{self.task_code_counter}"
        task = Task(
            id=self.task_id_counter,
            code=task_code,
            title=title,
            description=description,
            project_id=project_id,
            assignee_id=assignee_id
        )
        self.tasks[self.task_id_counter] = task
        self.task_id_counter += 1
        self.task_code_counter += 1
        return task

    def get_task_by_code(self, code: str) -> Optional[Task]:
        for task in self.tasks.values():
            if task.code == code:
                return task
        return None

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        return [task for task in self.tasks.values() if task.project_id == project_id]


# Глобальный БД
db = InMemoryDB()