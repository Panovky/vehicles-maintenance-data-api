import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

async_engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)