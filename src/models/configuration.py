import enum
from sqlalchemy import ForeignKey, Integer, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class EngineTypeEnum(enum.Enum):
    diesel = 'дизель'
    petrol = 'бензин'
    electricity = 'электричество'
    gas = 'газ'
    gas_petrol = 'газ/бензин'


class TransmissionEnum(enum.Enum):
    cvt = 'вариатор (CVT)'
    reducer = 'редуктор'
    robot = 'робот'
    manual = 'МКПП'
    automatic = 'АКПП'


class DriveEnum(enum.Enum):
    rear = 'задний привод'
    front = 'передний привод'
    full = 'полный привод (4WD)'


class Configuration(Base):
    __tablename__ = 'configurations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    engine_capacity: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    engine_power: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    engine_type: Mapped[EngineTypeEnum | None] = mapped_column(Enum(
        'дизель', 'бензин', 'электричество', 'газ', 'газ/бензин', name='enginetypeenum'
    ), nullable=True, default=None)
    transmission: Mapped[TransmissionEnum | None] = mapped_column(Enum(
        'вариатор (CVT)', 'редуктор', 'робот', 'МКПП', 'АКПП', name='transmissionenum'
    ), nullable=True, default=None)
    drive: Mapped[DriveEnum | None] = mapped_column(Enum(
        'задний привод', 'передний привод', 'полный привод (4WD)', name='driveenum'
    ), nullable=True, default=None)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'))
    generation = relationship('Generation', back_populates='configurations')
