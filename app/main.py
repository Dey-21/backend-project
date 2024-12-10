from fastapi import FastAPI
from app.database import Base, engine
from app.routes import db_test, users  
from app.models.user import User, Session

app = FastAPI()

# Incluir el enrutador para probar la conexión
app.include_router(db_test.router, prefix="/db")
app.include_router(users.router, prefix="/users", tags=["Users"]) 

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje": "API está funcionando!"}
