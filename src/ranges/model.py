from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.base_model import Base
from src.generations.model import Generation


class Range(Base):
    __tablename__ = 'ranges'

    name: Mapped[str] = mapped_column(String(70), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'))

    model = relationship('Model', back_populates='ranges')
    generations = relationship('Generation', back_populates='range')
    vehicles = relationship('Vehicle', back_populates='range')
