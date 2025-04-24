from fastapi import FastAPI
from app.routers.auth_router import router

app = FastAPI()

app.include_router(router)
