from logging.config import fileConfig
import asyncio
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "application"))

from infrastructure.postgres.database import Base
from src.application.infrastructure.postgres.models.users import *
from src.application.infrastructure.postgres.models.posts import *
from src.application.infrastructure.postgres.models.locations import *
from src.application.infrastructure.postgres.models.categories import *
from src.application.infrastructure.postgres.models.comments import *
from src.application.core.config import settings

from alembic import context

CREATE_SCHEMA_QUERY = f"CREATE SCHEMA IF NOT EXISTS {settings.POSTGRES_SCHEMA};"

config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


config.set_main_option("sqlalchemy.url", settings.postgres_url)


def filter_foreign_schemas(name, type_, parent_names):
    return type_ != "schema" or name == settings.POSTGRES_SCHEMA


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=settings.POSTGRES_SCHEMA,
        include_schemas=True,
        include_name=filter_foreign_schemas,
    )

    with context.begin_transaction():
        context.execute(CREATE_SCHEMA_QUERY)
        context.run_migrations()


async def run_migrations_online(engine: AsyncEngine):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    asyncio.run(run_migrations_online(connectable))