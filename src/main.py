from fastapi import FastAPI
from src.routes import users, services, makes, models, ranges, generations, configurations, scrape

app = FastAPI()

app.include_router(users.router)
app.include_router(services.router)
app.include_router(makes.router)
app.include_router(models.router)
app.include_router(ranges.router)
app.include_router(generations.router)
app.include_router(configurations.router)
app.include_router(scrape.router)
