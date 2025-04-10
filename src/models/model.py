import enum
from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities import Base


class ModelTypeEnum(enum.Enum):
    passenger = 'passenger'
    truck = 'truck'


class Model(Base):
    __tablename__ = 'models'

    name: Mapped[str] = mapped_column(String(40), nullable=False)
    type: Mapped[ModelTypeEnum] = mapped_column(Enum(ModelTypeEnum), nullable=False)
    make_id: Mapped[int] = mapped_column(Integer, ForeignKey('makes.id'))

    make = relationship('Make', back_populates='models')
    ranges = relationship('Range', back_populates='model')
    vehicles = relationship('Vehicle', back_populates='model')
