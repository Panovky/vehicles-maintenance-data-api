from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.auth.routes import router as auth_router
from src.users.routes import router as users_router
from src.user_roles.routes import router as user_roles_router
from src.makes.routes import router as makes_router
from src.models.routes import router as models_router
from src.ranges.routes import router as ranges_router
from src.generations.routes import router as generations_router
from src.configurations.routes import router as configurations_router
from src.scrapers.routes import router as scrapers_router
from src.vehicles.routes import router as vehicles_router
from src.services.routes import router as services_router
from src.service_workers.routes import router as service_workers_router
from src.service_clients.routes import router as service_clients_router
from src.maintenance_records.routes import router as maintenance_record_router

app = FastAPI(strict_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4173', 'http://127.0.0.1:4173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(user_roles_router)
app.include_router(makes_router)
app.include_router(models_router)
app.include_router(ranges_router)
app.include_router(generations_router)
app.include_router(configurations_router)
app.include_router(scrapers_router)
app.include_router(vehicles_router)
app.include_router(services_router)
app.include_router(service_workers_router)
app.include_router(service_clients_router)
app.include_router(maintenance_record_router)
