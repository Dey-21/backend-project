from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Usado para consultas asincrónicas
from app.database import SessionLocal, AsyncSessionLocal, AsyncSession, get_db
from app.schemas import UserRequest, UserLogin
from app.services.auth import authenticate_user, create_access_token
from app.models import User
from app.services.auth import hash_password

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

# Función asincrónica para agregar un usuario
async def add_user(db: AsyncSession, username: str, password: str):
    # Hashear la contraseña antes de guardarla
    hashed_password = hash_password(password)
    # Crear una instancia de usuario
    new_user = User(username=username, hashed_password=hashed_password)

# Agregar usuario de manera asincrónica
    db.add(new_user)
    await db.commit()  # Asincrónico, hace commit en la base de datos
    await db.refresh(new_user)  # Asincrónico, para obtener los datos más recientes
    return new_user

@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db_async)):
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Registro de usuario
@router.post('/register')
async def register(data: UserRequest, db: AsyncSession = Depends(get_db_async)):
    # Validar si el usuario ya existe
    query = select(User).where(User.username == data.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado."
        )

    # Llamar para agregar al usuario
    new_user = await add_user(db, data.username, data.password)
    return {"message": "Usuario registrado correctamente", "user_id": new_user.id}





