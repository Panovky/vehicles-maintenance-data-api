from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base


class Make(Base):
    __tablename__ = 'makes'

    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)

    models = relationship('Model', back_populates='make')
    vehicles = relationship('Vehicle', back_populates='make')
