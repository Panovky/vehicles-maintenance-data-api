from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class Range(Base):
    __tablename__ = 'ranges'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='ranges')
    generations = relationship('Generation', back_populates='range')
