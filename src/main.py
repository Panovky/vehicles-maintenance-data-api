from fastapi import FastAPI
from src.routes import users, services, vehicles

app = FastAPI()

app.include_router(users.router)
app.include_router(services.router)
app.include_router(vehicles.router)
