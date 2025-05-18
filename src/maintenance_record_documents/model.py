from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.base_model import Base


class MaintenanceRecordDocument(Base):
    __tablename__ = 'maintenance_record_documents'

    maintenance_record_id: Mapped[int] = mapped_column(Integer, ForeignKey('maintenance_records.id'))
    document_path: Mapped[str] = mapped_column(String(255), nullable=False)
