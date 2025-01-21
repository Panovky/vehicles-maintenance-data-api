import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)


class Base(DeclarativeBase):
    pass
