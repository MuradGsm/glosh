from fastapi import FastAPI
from app.routers.auth_router import auth_router
from app.routers.vacancy_router import vacancy_router
from app.routers.response_router import response_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(vacancy_router)
app.include_router(response_router)

