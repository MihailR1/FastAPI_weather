from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(url=settings.DATABASE_URL)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
