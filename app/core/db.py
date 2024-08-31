from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


