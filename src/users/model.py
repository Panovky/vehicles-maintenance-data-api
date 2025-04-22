import enum
from datetime import date
from sqlalchemy import Date, String, Integer, CHAR, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.base_model import Base


class RoleEnum(enum.Enum):
    owner = 'owner'
    worker = 'worker'
    manager = 'manager'
    admin = 'admin'


class User(Base):
    __tablename__ = 'users'

    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(40), nullable=True, default=None)
    birthday: Mapped[date | None] = mapped_column(Date, nullable=True, default=None)
    phone: Mapped[str | None] = mapped_column(CHAR(18), nullable=True, default=None, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    roles: Mapped[list['UserRole']] = relationship('UserRole', back_populates='user')


class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='roles')
