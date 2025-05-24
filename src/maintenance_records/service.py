import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from src.config import MAINTENANCE_RECORDS_PHOTOS_DIR, MAINTENANCE_RECORDS_DOCUMENTS_DIR
from src.maintenance_record_photos.repository import MaintenanceRecordPhotosRepository
from src.maintenance_record_documents.repository import MaintenanceRecordDocumentsRepository
from src.maintenance_record_workers.repository import MaintenanceRecordWorkersRepository
from src.service_workers.repository import ServiceWorkersRepository
from src.service_workers.schemas import ServiceWorkerRead
from src.vehicles.repository import VehiclesRepository
from src.maintenance_record_photos.schemas import MaintenanceRecordPhotoRead
from src.maintenance_record_documents.schemas import MaintenanceRecordDocumentRead
from src.exceptions import VehicleNotFoundException
from .repository import MaintenanceRecordsRepository
from .schemas import MaintenanceRecordRead
from .model import MaintenanceRecord, MaintenancePerformerEnum


class MaintenanceRecordsService:
    def __init__(
        self,
        maintenance_records_repository: MaintenanceRecordsRepository,
        maintenance_record_photos_repository: MaintenanceRecordPhotosRepository,
        maintenance_record_documents_repository: MaintenanceRecordDocumentsRepository,
        maintenance_record_workers_repository: MaintenanceRecordWorkersRepository,
        service_workers_repository: ServiceWorkersRepository,
        vehicles_repository: VehiclesRepository
    ):
        self.maintenance_records_repository: MaintenanceRecordsRepository = maintenance_records_repository
        self.maintenance_record_photos_repository: \
            MaintenanceRecordPhotosRepository = maintenance_record_photos_repository
        self.maintenance_record_documents_repository: \
            MaintenanceRecordDocumentsRepository = maintenance_record_documents_repository
        self.maintenance_record_workers_repository: \
            MaintenanceRecordWorkersRepository = maintenance_record_workers_repository
        self.service_workers_repository: ServiceWorkersRepository = service_workers_repository
        self.vehicles_repository: VehiclesRepository = vehicles_repository

    async def get_maintenance_record_read(self, maintenance_record: MaintenanceRecord) -> MaintenanceRecordRead:
        responsible = None
        service_workers = None

        if maintenance_record.maintenance_performer == MaintenancePerformerEnum.registered_service:
            res = await self.service_workers_repository.filter_by(
                service_id=maintenance_record.service_id,
                worker_id=maintenance_record.responsible.id
            )
            service_worker = res[0]
            responsible = ServiceWorkerRead(
                id=service_worker.worker.id,
                last_name=service_worker.worker.last_name,
                first_name=service_worker.worker.first_name,
                patronymic=service_worker.worker.patronymic,
                photo_path=service_worker.worker.photo_path,
                phone=service_worker.worker.phone,
                email=service_worker.worker.email,
                position=service_worker.position,
                rating=service_worker.rating
            )

            service_workers = []
            for maintenance_record_worker in maintenance_record.maintenance_record_workers:
                res = await self.service_workers_repository.filter_by(
                    service_id=maintenance_record.service_id,
                    worker_id=maintenance_record_worker.worker_id
                )
                service_worker = res[0]
                service_workers.append(ServiceWorkerRead(
                    id=service_worker.worker.id,
                    last_name=service_worker.worker.last_name,
                    first_name=service_worker.worker.first_name,
                    patronymic=service_worker.worker.patronymic,
                    photo_path=service_worker.worker.photo_path,
                    phone=service_worker.worker.phone,
                    email=service_worker.worker.email,
                    position=service_worker.position,
                    rating=service_worker.rating
                ))

        return MaintenanceRecordRead(
            title=maintenance_record.title,
            maintenance_performer=maintenance_record.maintenance_performer,
            date=maintenance_record.date,
            vehicle_id=maintenance_record.vehicle_id,
            mileage=maintenance_record.mileage,
            service_id=maintenance_record.service_id,
            responsible=responsible,
            description=maintenance_record.description,
            parts_cost=maintenance_record.parts_cost,
            labor_cost=maintenance_record.labor_cost,
            total_cost=maintenance_record.total_cost,
            photos=[MaintenanceRecordPhotoRead.model_validate(photo) for photo in maintenance_record.photos],
            documents=[MaintenanceRecordDocumentRead.model_validate(document) for document in
                       maintenance_record.documents],
            service_workers=service_workers
        )

    async def get_maintenance_records(self, vehicle_id: int) -> list[MaintenanceRecordRead]:
        if not await self.vehicles_repository.exists(id=vehicle_id):
            raise VehicleNotFoundException()

        maintenance_records = await self.maintenance_records_repository.filter_by(vehicle_id=vehicle_id)
        return [
            await self.get_maintenance_record_read(maintenance_record) for maintenance_record in maintenance_records
        ]

    async def create(
            self,
            data: dict,
            photos: list[UploadFile] | None,
            documents: list[UploadFile] | None,
            workers_ids: str | None
    ) -> MaintenanceRecordRead:
        maintenance_record = await self.maintenance_records_repository.create(data)

        if photos:
            for photo in photos:
                photo_name = f'{uuid.uuid4().hex}{Path(photo.filename).suffix}'
                photo_path = MAINTENANCE_RECORDS_PHOTOS_DIR / photo_name
                async with aiofiles.open(photo_path, 'wb') as buffer:
                    while chunk := await photo.read(1024):
                        await buffer.write(chunk)
                await self.maintenance_record_photos_repository.create({
                    'maintenance_record_id': maintenance_record.id,
                    'photo_path': f'/static/maintenance_records/photos/{photo_name}'
                })

        if documents:
            for document in documents:
                document_name = f'{uuid.uuid4().hex}{Path(document.filename).suffix}'
                document_path = MAINTENANCE_RECORDS_DOCUMENTS_DIR / document_name
                async with aiofiles.open(document_path, 'wb') as buffer:
                    while chunk := await document.read(1024):
                        await buffer.write(chunk)
                await self.maintenance_record_documents_repository.create({
                    'maintenance_record_id': maintenance_record.id,
                    'document_path': f'/static/maintenance_records/documents/{document_name}'
                })

        if workers_ids:
            for worker_id in map(int, workers_ids.split(', ')):
                await self.maintenance_record_workers_repository.create({
                    'maintenance_record_id': maintenance_record.id,
                    'worker_id': worker_id
                })

        return await self.get_maintenance_record_read(maintenance_record)


