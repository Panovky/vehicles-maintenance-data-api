import os
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated

async_engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
