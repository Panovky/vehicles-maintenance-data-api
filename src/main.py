from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.routes import router as auth_router
from src.users.routes import router as users_router
from src.services.routes import router as services_router
from src.scrapers.routes import router as scrape_router

app = FastAPI(strict_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4173', 'http://127.0.0.1:4173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(services_router)
app.include_router(scrape_router)
