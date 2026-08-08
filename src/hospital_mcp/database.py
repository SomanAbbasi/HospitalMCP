from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from hospital_mcp.config import settings


engine = create_engine(
    settings.database_url,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass
