import enum
from datetime import date, datetime
from sqlalchemy import Integer, DateTime, Date, String, CHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class UserRoleEnum(str, enum.Enum):
    owner = 'owner'
    employee = 'employee'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(40), nullable=True, default=None)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(CHAR(18), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)
    login: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
