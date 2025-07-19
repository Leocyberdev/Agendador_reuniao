import os
from logging.config import fileConfig
from dotenv import load_dotenv

from alembic import context
from sqlalchemy import create_engine, pool

# Carrega o .env (ajuste o caminho se seu .env estiver em outro lugar)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'src', '.env'))

# Importa a app e os metadados do SQLAlchemy
from src import create_app
from src.models import db

# Inicializa a app
app = create_app()

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL do banco de dados vinda do .env
database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
if not database_url:
    raise RuntimeError("❌ SQLALCHEMY_DATABASE_URI não encontrada no .env")

print("✅ Banco de dados:", database_url)

# Metadados dos modelos
target_metadata = db.metadata

def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = create_engine(database_url, poolclass=pool.NullPool)
    with app.app_context():
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
