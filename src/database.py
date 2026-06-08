from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import Engine, create_engine, URL
from sqlalchemy.orm import Session, sessionmaker

from config.config import get_settings

SYNC_ENGINE_OPTIONS = {
    "echo": False,
    "pool_size": 30,
    "max_overflow": 45,
    "pool_pre_ping": True,
}

Url = URL.create(
    drivername="iris+intersystems",
    username=get_settings().DB_USER,
    password=get_settings().DB_PASSWORD,
    host=get_settings().DB_HOST,
    port=get_settings().DB_PORT,
    database=get_settings().DB_NAMESPACE
)

@lru_cache
def get_iris_engine() -> Engine:
    return create_engine(Url, **SYNC_ENGINE_OPTIONS)


@lru_cache
def get_iris_session_factory() -> sessionmaker[Session]:
    return sessionmaker(
        bind=get_iris_engine(),
        class_=Session,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


def get_db() -> Generator[Session, None, None]:
    session = get_iris_session_factory()()
    try:
        yield session
    finally:
        session.close()


async def dispose_database_connections() -> None:
    if get_iris_engine.cache_info().currsize:
        get_iris_engine().dispose()