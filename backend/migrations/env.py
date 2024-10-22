import asyncio
from logging.config import fileConfig
from typing import Any, Callable

from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context

from app.infra.config import settings
from app.data.models import Model


# TODO: Function to get tenant schemas
def get_tenant_schemas() -> list[str]:
    return ['tenant1', 'tenant2', 'default']

# TODO: Define a suitable scenario for using it
def include_name_for_schema(schema_name: str) -> Callable[[Any, Any, dict[str, str]], bool]:
    def include_name(name: str, type_: str, parent_names: dict[str, str]) -> bool:
        if parent_names['schema'] == schema_name:
            return True
        return False
    return include_name

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Model.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    for schema_name in get_tenant_schemas():
        context.configure(
            url = settings.get_postgres_dsn(schema_name, "asyncpg"),
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,
        )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection, schema_name): #  type: ignore
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
        version_table_schema=schema_name,
        # include_name=include_name_for_schema(schema_name),
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    if not configuration:
        raise ValueError("No Alembic config found")

    for schema_name in get_tenant_schemas():
        connectable = async_engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
            # debug=True,
        )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations, schema_name=schema_name)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
