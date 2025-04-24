from fastapi import APIRouter, status
from src.dependencies import CurrentManagerDep, ServicesServiceDep
from .schemas import ServiceRead, ServiceCreate

router = APIRouter(
    prefix='/services',
    tags=['services']
)
