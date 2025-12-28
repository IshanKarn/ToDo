from fastapi import FastAPI
from app.database import init_db
from app.routes import auth_ui,auth_api, tasks_api, tasks_ui
import logging

logging.basicConfig(
    filename="app/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="To-Do App")

init_db()

app.include_router(auth_ui.router)    
app.include_router(tasks_ui.router)
app.include_router(auth_api.router)
app.include_router(tasks_api.router)
