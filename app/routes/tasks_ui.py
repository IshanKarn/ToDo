from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth import get_logged_in_user
from app import crud

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    user_id = get_logged_in_user(request)

    if not user_id:
        return RedirectResponse("/login", status_code=302)

    tasks = crud.get_tasks(user_id)

    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "tasks": tasks,
            "is_logged_in": True   # ✅ pass explicitly
        }
    )

@router.post("/tasks/create")
def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    due_date: str = Form(None)
):
    user_id = get_logged_in_user(request)
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    crud.create_task(
        {
            "title": title,
            "description": description,
            "due_date": due_date
        },
        user_id
    )

    return RedirectResponse("/", status_code=303)

@router.post("/tasks/update/{task_id}")
def update_task(
    request: Request,
    task_id: int,
    status: str = Form(...)
):
    user_id = get_logged_in_user(request)
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    crud.update_task(
        task_id,
        user_id,
        {"status": status}
    )

    return RedirectResponse("/", status_code=303)

@router.post("/tasks/delete/{task_id}")
def delete_task(request: Request, task_id: int):
    user_id = get_logged_in_user(request)
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    crud.delete_task(task_id, user_id)
    return RedirectResponse("/", status_code=303)