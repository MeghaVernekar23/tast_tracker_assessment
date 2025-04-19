from fastapi import FastAPI
from api.users import user_router
from api.tasks import task_router
from api.documents import document_router

app = FastAPI(title="Task Tracker API",
    description="Task Tracker API",)


app.include_router(user_router,prefix="/users")
app.include_router(task_router,prefix="/tasks")
app.include_router(document_router,prefix="/documents")