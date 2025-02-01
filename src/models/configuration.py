from sqlalchemy import ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class Configuration(Base):
    __tablename__ = 'configurations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    engine_capacity: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    engine_power: Mapped[int] = mapped_column(Integer, nullable=False)
    engine_type: Mapped[str] = mapped_column(String(30), nullable=False)
    transmission: Mapped[str] = mapped_column(String(30), nullable=False)
    drive: Mapped[str] = mapped_column(String(30), nullable=False)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'))
    generation = relationship('Generation', back_populates='configurations')
