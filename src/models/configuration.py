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

    engine_capacity: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    engine_power: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    engine_type: Mapped[EngineTypeEnum | None] = mapped_column(
        Enum(*[elem.value for elem in EngineTypeEnum], name='enginetypeenum'), nullable=True, default=None
    )
    transmission: Mapped[TransmissionEnum | None] = mapped_column(
        Enum(*[elem.value for elem in TransmissionEnum], name='transmissionenum'), nullable=True, default=None
    )
    drive: Mapped[DriveEnum | None] = mapped_column(
        Enum(*[elem.value for elem in DriveEnum], name='driveenum'), nullable=True, default=None
    )
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'))

    generation = relationship('Generation', back_populates='configurations')
    vehicles = relationship('Vehicle', back_populates='configuration')
