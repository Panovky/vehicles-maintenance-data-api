from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.utils.base_model import Base


class Service(Base):
    __tablename__ = 'services'

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    ogrn: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None)
    timetable: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    manager_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
