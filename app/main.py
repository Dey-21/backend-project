import asyncio
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import db_test, users  
from app.models.user import User, Session

app = FastAPI()

# Incluir el enrutador para probar la conexión
app.include_router(db_test.router, prefix="/db")
app.include_router(users.router, prefix="/users", tags=["Users"]) 

# Crear las tablas asincrónicamente
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    # Ejecutar la creación de tablas cuando la aplicación se inicie
    await create_tables()

@app.get("/")
def read_root():
    return {"mensaje": "API está funcionando!"}
