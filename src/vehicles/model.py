import enum
from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.base_model import Base


class VehicleColorEnum(enum.Enum):
    white = 'белый'
    beige = 'бежевый'
    yellow = 'желтый'
    gold = 'золотистый'
    orange = 'оранжевый'
    pink = 'розовый'
    red = 'красный'
    burgundy = 'бордовый'
    green = 'зеленый'
    light_blue = 'голубой'
    blue = 'синий'
    purple = 'фиолетовый'
    grey = 'серый'
    silver = 'серебристый'
    brown = 'коричневый'
    black = 'черный'


class Vehicle(Base):
    __tablename__ = 'vehicles'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    make_id: Mapped[int] = mapped_column(Integer, ForeignKey('makes.id'))
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'))
    range_id: Mapped[int] = mapped_column(Integer, ForeignKey('ranges.id'))
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey('generations.id'))
    configuration_id: Mapped[int] = mapped_column(Integer, ForeignKey('configurations.id'))
    color: Mapped[VehicleColorEnum] = mapped_column(
        Enum(*[elem.value for elem in VehicleColorEnum], name='vehiclecolorenum'), nullable=False
    )
    manufacture_year: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    vin: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    registration_number: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)

    make = relationship('Make', back_populates='vehicles')
    model = relationship('Model', back_populates='vehicles')
    range = relationship('Range', back_populates='vehicles')
    generation = relationship('Generation', back_populates='vehicles')
    configuration = relationship('Configuration', back_populates='vehicles')
