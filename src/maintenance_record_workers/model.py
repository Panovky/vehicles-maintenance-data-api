from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import Base


class MaintenanceRecordWorker(Base):
    __tablename__ = 'maintenance_record_workers'

    maintenance_record_id: Mapped[int] = mapped_column(Integer, ForeignKey('maintenance_records.id'))
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    worker = relationship('User', back_populates='maintenance_record_workers')
    maintenance_record = relationship('MaintenanceRecord', back_populates='maintenance_record_workers')

