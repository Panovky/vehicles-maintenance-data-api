from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.models import BaseModel


class Service(BaseModel):
    __tablename__ = 'services'

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None)
    timetable: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
