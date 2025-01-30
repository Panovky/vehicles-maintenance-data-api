from fastapi import FastAPI
from src.routes import users, services, makes, models, ranges, generations, configurations

app = FastAPI()

app.include_router(users.router)
app.include_router(services.router)
app.include_router(makes.router)
app.include_router(models.router)
app.include_router(ranges.router)
app.include_router(generations.router)
app.include_router(configurations.router)
