from datetime import datetime
from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None)
    timetable: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
