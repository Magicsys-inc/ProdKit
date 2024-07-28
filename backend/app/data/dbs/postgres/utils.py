from sqlalchemy import inspect
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.schema import CreateSchema

from app.infra.config import settings


async def create_schema(engine: AsyncEngine, schema_name: str) -> None:
    async with engine.connect() as conn:
        inspector = inspect(conn)
        if inspector and not await inspector.has_schema(schema_name):
            try:
                await conn.execute(CreateSchema(schema_name))  # type: ignore
            except ProgrammingError as e:
                if "already exists" not in str(e):
                    raise


async def create_special_schema(engine: AsyncEngine) -> None:
    special_schema: str = settings.SPECIAL_SCHEMA
    await create_schema(engine, special_schema)


async def create_tenant_schema(engine: AsyncEngine, tenant_id: str) -> None:
    tenant_schema: str = f"tenant_{tenant_id}"
    await create_schema(engine, tenant_schema)
