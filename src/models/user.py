import enum
from datetime import date
from sqlalchemy import Date, String, CHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class UserRoleEnum(enum.Enum):
    owner = 'owner'
    employee = 'employee'


class User(Base):
    __tablename__ = 'users'

    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(40), nullable=True, default=None)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(CHAR(18), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)
    login: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)

    vehicles = relationship('Vehicle', back_populates='user')
