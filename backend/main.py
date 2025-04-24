from fastapi import FastAPI
from api.users import user_router
from api.tasks import task_router
from api.documents import document_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Task Tracker API",
    description="Task Tracker API",)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(task_router,prefix="/tasks")
app.include_router(document_router,prefix="/documents")