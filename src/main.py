from fastapi import FastAPI
from src.routes import users, services

app = FastAPI()

app.include_router(users.router)
app.include_router(services.router)
