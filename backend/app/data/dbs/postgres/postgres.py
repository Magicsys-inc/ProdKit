from typing import TypeAlias

from sqlalchemy import Engine
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine as _create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from .extensions.sqlalchemy import sql


class EngineFactory:
    @staticmethod
    def create_async_engine(
        *,
        dsn: str,
        application_name: str | None = None,
        pool_size: int | None = None,
        pool_recycle: int | None = None,
        debug: bool = False,
    ) -> AsyncEngine:
        return _create_async_engine(
            dsn,
            echo=debug,
            connect_args={"server_settings": {"application_name": application_name}}
            if application_name
            else {},
            pool_size=pool_size,
            pool_recycle=pool_recycle,
        )

    @staticmethod
    def create_sync_engine(
        *,
        dsn: str,
        application_name: str | None = None,
        pool_size: int | None = None,
        pool_recycle: int | None = None,
        debug: bool = False,
    ) -> Engine:
        return _create_engine(
            dsn,
            echo=debug,
            connect_args={"application_name": application_name}
            if application_name
            else {},
            pool_size=pool_size,
            pool_recycle=pool_recycle,
        )


AsyncSessionMaker: TypeAlias = async_sessionmaker[AsyncSession]
SyncSessionMaker: TypeAlias = sessionmaker[Session]


class SessionMakerFactory:
    @staticmethod
    def create_async_sessionmaker(
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    @staticmethod
    def create_sync_sessionmaker(engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(engine, expire_on_commit=False)


__all__ = [
    "AsyncSession",
    "AsyncEngine",
    "Session",
    "Engine",
    "AsyncSessionMaker",
    "SyncSessionMaker",
    "EngineFactory",
    "SessionMakerFactory",
    "sql",
]
