from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Credenciales de la base de datos
DATABASE_URL = "postgresql+asyncpg://admin21:d210e280y@proyecto.cnqowac8sq1o.eu-north-1.rds.amazonaws.com:5432/proyecto"

# Configuración del motor SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Creación de la base declarativa
Base = declarative_base()

# Configuración de la sesión asincrónica
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, autocommit=False
)

# Función para obtener la sesión local
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Sesiones síncronas
sync_engine = create_engine("postgresql://admin21:d210e280y@proyecto.cnqowac8sq1o.eu-north-1.rds.amazonaws.com:5432/proyecto")

# Configuración de la sesión síncrona
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)