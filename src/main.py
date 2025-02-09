from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import users, services, makes, models, ranges, generations, configurations, scrape, vehicles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users.router)
app.include_router(services.router)
app.include_router(makes.router)
app.include_router(models.router)
app.include_router(ranges.router)
app.include_router(generations.router)
app.include_router(configurations.router)
app.include_router(scrape.router)
app.include_router(vehicles.router)
