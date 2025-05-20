from datetime import date
from sqlalchemy import Date, String, CHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import Base


class User(Base):
    __tablename__ = 'users'

    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(40), nullable=True, default=None)
    photo_path: Mapped[str] = mapped_column(String(255), nullable=False, default='/static/users/photos/default.png')
    birthday: Mapped[date | None] = mapped_column(Date, nullable=True, default=None)
    phone: Mapped[str | None] = mapped_column(CHAR(18), nullable=True, default=None, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False)

    roles = relationship('UserRole', back_populates='user')
