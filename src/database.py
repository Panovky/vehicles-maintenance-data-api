import os
from datetime import datetime
from fastapi import Depends
from sqlalchemy import Integer, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated

async_engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
