from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.base_model import Base


class MaintenanceRecordWorker(Base):
    __tablename__ = 'maintenance_record_workers'

    maintenance_record_id: Mapped[int] = mapped_column(Integer, ForeignKey('maintenance_records.id'))
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey('service_workers.id'))
