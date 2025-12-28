from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routes import auth_ui,auth_api, tasks_api, tasks_ui
import logging
from starlette.middleware.sessions import SessionMiddleware

logging.basicConfig(
    filename="app/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="To-Do App")

# 🔐 Session middleware (MUST be before routes)
app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

init_db()

app.include_router(auth_ui.router)    
app.include_router(tasks_ui.router)
app.include_router(auth_api.router)
app.include_router(tasks_api.router)
