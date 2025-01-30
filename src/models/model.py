from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    make_id: Mapped[int] = mapped_column(Integer, ForeignKey('makes.id'))
    make = relationship('Make', back_populates='models')
    ranges = relationship('Range', back_populates='model')
