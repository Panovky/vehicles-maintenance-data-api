import enum
from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.base_model import Base


class UserRoleEnum(enum.Enum):
    owner = 'owner'
    worker = 'worker'
    manager = 'manager'
    admin = 'admin'


class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)

    user = relationship('User', back_populates='roles')
