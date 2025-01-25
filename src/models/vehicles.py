from pydantic import HttpUrl
from sqlalchemy import ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class Make(Base):
    __tablename__ = 'makes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    models = relationship('Model', back_populates='make')


class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    make_id: Mapped[int] = mapped_column(Integer, ForeignKey('makes.id'))
    make = relationship('Make', back_populates='models')
    ranges = relationship('Range', back_populates='model')


class Range(Base):
    __tablename__ = 'ranges'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='ranges')
    generations = relationship('Generation', back_populates='range')


class Generation(Base):
    __tablename__ = 'generations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photo_url: Mapped[HttpUrl] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    short_name: Mapped[str] = mapped_column(String(30), nullable=False)
    vehicle_body: Mapped[str] = mapped_column(String(30), nullable=False)
    range_id: Mapped[int] = mapped_column(Integer, ForeignKey('ranges.id'))
    range = relationship('Range', back_populates='generations')
    configurations = relationship('Configuration', back_populates='generation')


class Configuration(Base):
    __tablename__ = 'configurations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    engine_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    engine_power: Mapped[int] = mapped_column(Integer, nullable=False)
    engine_type: Mapped[str] = mapped_column(String(30), nullable=False)
    transmission: Mapped[str] = mapped_column(String(30), nullable=False)
    drive: Mapped[str] = mapped_column(String(30), nullable=False)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'))
    generation = relationship('Generation', back_populates='configurations')

