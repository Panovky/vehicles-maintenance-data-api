from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import Base


class ServiceWorker(Base):
    __tablename__ = 'service_workers'

    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('services.id'))
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    ratings_sum: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ratings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    worker = relationship('User', back_populates='service_workers')
    maintenance_records = relationship('MaintenanceRecord', back_populates='responsible')
    maintenance_record_service_workers = relationship('MaintenanceRecordServiceWorker', back_populates='service_worker')
