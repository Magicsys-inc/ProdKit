from collections.abc import AsyncGenerator
from typing import Literal, TypeAlias

from fastapi import Depends, Request

from app.data.dbs.postgres.postgres import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionMaker,
    Engine,
    EngineFactory,
    Session,
    SessionMakerFactory,
    SyncSessionMaker,
    sql,
)
from app.infra.config import settings

ProcessName: TypeAlias = Literal["app", "worker", "script"]


class DatabaseEngine:
    @staticmethod
    def create_async_engine(
        process_name: ProcessName, tenant_id: str | None
    ) -> AsyncEngine:
        dsn = settings.get_postgres_dsn(tenant_id, "asyncpg")
        return EngineFactory.create_async_engine(
            dsn=dsn,
            application_name=f"{settings.ENV.value}.{process_name}",
            debug=settings.DEBUG,
            pool_size=settings.DATABASE_POOL_SIZE,
            pool_recycle=settings.DATABASE_POOL_RECYCLE_SECONDS,
        )

    @staticmethod
    def create_sync_engine(process_name: ProcessName, tenant_id: str | None) -> Engine:
        dsn = settings.get_postgres_dsn(tenant_id, "psycopg2")
        return EngineFactory.create_sync_engine(
            dsn=dsn,
            application_name=f"{settings.ENV.value}.{process_name}",
            debug=settings.DEBUG,
            pool_size=settings.DATABASE_SYNC_POOL_SIZE,
            pool_recycle=settings.DATABASE_POOL_RECYCLE_SECONDS,
        )


class DatabaseSession:
    @staticmethod
    async def get_db_sessionmaker(
        request: Request,
    ) -> AsyncGenerator[AsyncSessionMaker, None]:
        async_sessionmaker: AsyncSessionMaker = request.state.async_sessionmaker
        yield async_sessionmaker

    default_async_sessionmaker = Depends(get_db_sessionmaker)

    @staticmethod
    async def get_db_session(
        request: Request,
        sessionmaker: AsyncSessionMaker = default_async_sessionmaker,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Generates a new session for the request using the sessionmaker in the application state.
        Note that we store it in the request state: this way, we make sure we only have
        one session per request.
        """
        if session := getattr(request.state, "session", None):
            yield session
        else:
            async with sessionmaker() as session:
                try:
                    request.state.session = session
                    yield session
                except:
                    await session.rollback()
                    raise
                else:
                    await session.commit()


__all__ = [
    "Engine",
    "AsyncEngine",
    "EngineFactory",
    "DatabaseEngine",
    "Session",
    "AsyncSession",
    "SyncSessionMaker",
    "AsyncSessionMaker",
    "SessionMakerFactory",
    "DatabaseSession",
    "sql",
]
