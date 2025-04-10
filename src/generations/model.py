from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities import Base


class Generation(Base):
    __tablename__ = 'generations'

    photo_url: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name: Mapped[str] = mapped_column(String(30), nullable=False)
    vehicle_body: Mapped[str] = mapped_column(String(30), nullable=False)
    range_id: Mapped[int] = mapped_column(Integer, ForeignKey('ranges.id'))

    range = relationship('Range', back_populates='generations')
    configurations = relationship('Configuration', back_populates='generation')
    vehicles = relationship('Vehicle', back_populates='generation')
