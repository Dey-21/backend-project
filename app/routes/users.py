from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, AsyncSessionLocal, AsyncSession
from app.services import add_user
from app.schemas import UserRequest

#Enrutador con el prefijo "/user"
router = APIRouter(prefix="/user")

# Dependencia para obtener la sesión sincrónico
def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()

# Dependencia para obtener la sesión asincrónico
async def get_db_async():
    async with AsyncSessionLocal() as session:
        yield session

#registro de usuario
@router.post('/register')
async def register(data: UserRequest, db: AsyncSession = Depends(get_db_async)):
    username = data.username
    password = data.password

    return await add_user(db, username, password)