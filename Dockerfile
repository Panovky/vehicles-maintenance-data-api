FROM python:3.11

WORKDIR /VehiclesMaintenanceDataAPI

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY alembic.ini .