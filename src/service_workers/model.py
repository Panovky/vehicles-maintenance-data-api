from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.base_model import Base


class ServiceWorker(Base):
    __tablename__ = 'service_workers'

    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('services.id'))
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0)
