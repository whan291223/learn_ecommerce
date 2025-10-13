from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionFactory = sessionmaker( # use session for query, add newdata, savechanges
    engine,
    class_ = AsyncSession,
    expire_on_commit=False #after commit data still available even the session is expire
)