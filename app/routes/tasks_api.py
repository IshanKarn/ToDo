from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TaskCreate, TaskUpdate
from app.auth import verify_token
from app import crud

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("/")
def create_task(task: TaskCreate, token=Depends(verify_token)):
    user_id = token["user_id"]
    return crud.create_task(task.dict(), user_id)

@router.get("/")
def list_tasks(token=Depends(verify_token)):
    return crud.get_tasks(token["user_id"])


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    token=Depends(verify_token)
):
    result = crud.update_task(task_id, token["user_id"], task.dict())

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return result


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    token=Depends(verify_token)
):
    result = crud.delete_task(task_id, token["user_id"])

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return result
