from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import Base


class MaintenanceRecordPhoto(Base):
    __tablename__ = 'maintenance_record_photos'

    maintenance_record_id: Mapped[int] = mapped_column(Integer, ForeignKey('maintenance_records.id'))
    photo_path: Mapped[str] = mapped_column(String(255), nullable=False)

    maintenance_record = relationship('MaintenanceRecord', back_populates='photos')
