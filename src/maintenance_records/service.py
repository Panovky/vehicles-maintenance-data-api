import aiofiles
from pathlib import Path
from fastapi import UploadFile
from src.config import MAINTENANCE_RECORDS_PHOTOS_DIR, MAINTENANCE_RECORDS_DOCUMENTS_DIR
from src.maintenance_record_photos.repository import MaintenanceRecordPhotosRepository
from src.maintenance_record_documents.repository import MaintenanceRecordDocumentsRepository
from src.maintenance_record_service_workers.repository import MaintenanceRecordWorkersRepository
from src.service_workers.schemas import ServiceWorkerRead
from src.maintenance_record_photos.schemas import MaintenanceRecordPhotoRead
from src.maintenance_record_documents.schemas import MaintenanceRecordDocumentRead
from .repository import MaintenanceRecordsRepository
from .schemas import MaintenanceRecordRead


class MaintenanceRecordsService:
    def __init__(
        self,
        maintenance_records_repository: MaintenanceRecordsRepository,
        maintenance_record_photos_repository: MaintenanceRecordPhotosRepository,
        maintenance_record_documents_repository: MaintenanceRecordDocumentsRepository,
        maintenance_record_workers_repository: MaintenanceRecordWorkersRepository
    ):
        self.maintenance_records_repository: MaintenanceRecordsRepository = maintenance_records_repository
        self.maintenance_record_photos_repository: \
            MaintenanceRecordPhotosRepository = maintenance_record_photos_repository
        self.maintenance_record_documents_repository: \
            MaintenanceRecordDocumentsRepository = maintenance_record_documents_repository
        self.maintenance_record_workers_repository: \
            MaintenanceRecordWorkersRepository = maintenance_record_workers_repository

    async def create(
            self,
            data: dict,
            photos: list[UploadFile] | None,
            documents: list[UploadFile] | None,
            service_workers_ids: str | None
    ) -> MaintenanceRecordRead:
        maintenance_record = await self.maintenance_records_repository.create(data)

        if photos:
            for photo in photos:
                photo_name = f'{maintenance_record.id}{Path(photo.filename).suffix}'
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
                document_name = f'{maintenance_record.id}{Path(document.filename).suffix}'
                document_path = MAINTENANCE_RECORDS_DOCUMENTS_DIR / document_name
                async with aiofiles.open(document_path, 'wb') as buffer:
                    while chunk := await document.read(1024):
                        await buffer.write(chunk)
                await self.maintenance_record_documents_repository.create({
                    'maintenance_record_id': maintenance_record.id,
                    'document_path': f'/static/maintenance_records/documents/{document_name}'
                })

        if service_workers_ids:
            for service_worker_id in map(int, service_workers_ids.split(',')):
                await self.maintenance_record_workers_repository.create({
                    'maintenance_record_id': maintenance_record.id,
                    'service_worker_id': service_worker_id
                })

        maintenance_record = await self.maintenance_records_repository.get_by_id(maintenance_record.id)
        return MaintenanceRecordRead(
            title=maintenance_record.title,
            maintenance_performer=maintenance_record.maintenance_performer,
            date=maintenance_record.date,
            vehicle_id=maintenance_record.vehicle_id,
            mileage=maintenance_record.mileage,
            service_id=maintenance_record.service_id,
            responsible=ServiceWorkerRead(
                last_name=maintenance_record.responsible.user.last_name,
                first_name=maintenance_record.responsible.user.first_name,
                patronymic=maintenance_record.responsible.user.patronymic,
                photo_path=maintenance_record.responsible.user.photo_path,
                phone=maintenance_record.responsible.user.phone,
                email=maintenance_record.responsible.user.email,
                position=maintenance_record.responsible.position,
                rating=maintenance_record.responsible.rating
            ),
            description=maintenance_record.description,
            parts_cost=maintenance_record.parts_cost,
            labor_cost=maintenance_record.labor_cost,
            total_cost=maintenance_record.total_cost,
            photos=[MaintenanceRecordPhotoRead.model_validate(photo) for photo in maintenance_record.photos],
            documents=[MaintenanceRecordDocumentRead.model_validate(document) for document in maintenance_record.documents],
            service_workers=[ServiceWorkerRead(
                last_name=maintenance_record_service_worker.service_worker.user.last_name,
                first_name=maintenance_record_service_worker.service_worker.user.first_name,
                patronymic=maintenance_record_service_worker.service_worker.user.patronymic,
                photo_path=maintenance_record_service_worker.service_worker.user.photo_path,
                phone=maintenance_record_service_worker.service_worker.user.phone,
                email=maintenance_record_service_worker.service_worker.user.email,
                position=maintenance_record_service_worker.service_worker.position,
                rating=maintenance_record_service_worker.service_worker.rating
            ) for maintenance_record_service_worker in maintenance_record.maintenance_record_service_workers]
        )

