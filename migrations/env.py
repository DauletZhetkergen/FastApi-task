from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy import MetaData
from app.config import DB_NAME, DB_PORT, DB_PASSWORD, DB_USER, DB_HOST
from app.models import Base
from app.models.users import UserModel
from app.models.order import OrderModel


target_metadata = [Base.metadata]
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASS", DB_PASSWORD)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)

fileConfig(config.config_file_name)



if config.config_file_name is not None:
    fileConfig(config.config_file_name)



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


run_migrations_online()
