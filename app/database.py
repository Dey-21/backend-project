from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Credenciales de la base de datos
DATABASE_URL = "postgresql://admin21:d210e280y@proyecto.cnqowac8sq1o.eu-north-1.rds.amazonaws.com:5432/proyecto"

# Configuración del motor SQLAlchemy
engine = create_engine(DATABASE_URL)

# Creación de la base declarativa
Base = declarative_base()

# Configuración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
