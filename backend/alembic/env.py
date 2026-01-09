from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

def get_database_url():
    """
    Получаем URL БД и конвертируем для Alembic
    Alembic нужен СИНХРОННЫЙ драйвер (psycopg2)
    """
    db_url = os.getenv("DATABASE_URL_LOCAL")

    if db_url:
        # Alembic не работает с asyncpg, нужен psycopg2
        if "+asyncpg" in db_url:
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
            print("★ Converted asyncpg → psycopg2 for Alembic")
        
        # Добавляем порт если нужно
        if "://" in db_url and "@" in db_url:
            parts = db_url.split("@", 1)
            host_db_part = parts[1]
            
            if ":" not in host_db_part.split("/")[0] and ".render.com" not in host_db_part:
                host_part = host_db_part.split("/")[0]
                db_part = "/".join(host_db_part.split("/")[1:])
                db_url = f"{parts[0]}@{host_part}:5432/{db_part}"
        
        print(f"★ Alembic will use: {db_url.split('@')[0]}@***")
        return db_url
    
    default_url = "postgresql://postgres:postgres@postgres:5432/microservice_db"
    return default_url

config.set_main_option("sqlalchemy.url", get_database_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata



def run_migrations_offline() -> None:
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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
