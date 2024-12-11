from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Credenciales de la base de datos motor sincrónico
DATABASE_URL = "postgresql://admin21:d210e280y@proyecto.cnqowac8sq1o.eu-north-1.rds.amazonaws.com:5432/proyecto"

# Credenciales de la base de datos motor asincrónico
DATABASE_URL_AS = "postgresql+asyncpg://admin21:d210e280y@proyecto.cnqowac8sq1o.eu-north-1.rds.amazonaws.com:5432/proyecto"

# Configuración del motor SQLAlchemy sincrónico
engine = create_engine(DATABASE_URL)

# Configuración del motor SQLAlchemy asincrónico
async_engine = create_engine(DATABASE_URL_AS)

# Creación de la base declarativa
Base = declarative_base()

# Configuración de la sesión sincrónico
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configuración de la sesión asincrónico
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
