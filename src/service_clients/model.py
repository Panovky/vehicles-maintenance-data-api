from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.base_model import Base


class ServiceClient(Base):
    __tablename__ = 'service_clients'

    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('services.id'))
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
