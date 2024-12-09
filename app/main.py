from app.database import Base, engine
from app.models.user import User

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)

print("Tablas creadas con éxito.")
