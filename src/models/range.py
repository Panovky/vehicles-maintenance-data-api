from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel


class Range(BaseModel):
    __tablename__ = 'ranges'

    name: Mapped[str] = mapped_column(String(70), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='ranges')
    generations = relationship('Generation', back_populates='range')
