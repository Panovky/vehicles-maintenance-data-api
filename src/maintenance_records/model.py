import enum
from datetime import date
from sqlalchemy import String, Date, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.base_model import Base


class MaintenancePerformerEnum(enum.Enum):
    owner = 'owner'
    unregistered_service = 'unregistered_service'
    registered_service = 'registered_service'


class MaintenanceRecord(Base):
    __tablename__ = 'maintenance_records'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    maintenance_performer: Mapped[MaintenancePerformerEnum] = mapped_column(
        Enum(MaintenancePerformerEnum), nullable=False
    )
    service_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('services.id'), nullable=True, default=None)
    responsible_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('users.id'), nullable=True, default=None)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id'))
    mileage: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True, default=None)
    parts_cost: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    labor_cost: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_cost: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

