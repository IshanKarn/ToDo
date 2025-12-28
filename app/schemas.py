from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: str | None = None

class TaskResponse(TaskCreate):
    id: int
    status: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None