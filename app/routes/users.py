from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Usado para consultas asincrónicas
from app.database import SessionLocal, AsyncSessionLocal, AsyncSession, get_db
from app.schemas import UserRequest, UserLogin
from app.services.auth import authenticate_user, hash_password, create_session, create_access_token 
from app.models import User
import re


#Enrutador con el prefijo "/user"
router = APIRouter(prefix="/user")

# Dependencia para obtener la sesión asincrónico
async def get_db_async():
    async with AsyncSessionLocal() as session:
        yield session

def format_phone_number(phone_number: str) -> str:
    # Formato deseado: +00 000 00 00 00
    cleaned_number = re.sub(r'\D', '', phone_number)
    formatted_phone = f"+{cleaned_number[:2]} {cleaned_number[2:5]} {cleaned_number[5:7]} {cleaned_number[7:9]} {cleaned_number[9:]}"
    return formatted_phone

# Endpoint de inicio de sesión
@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    
     # Crear sesión y guardar el token
    session = await create_session(db, user.id)

    # Crear el token JWT
    access_token = create_access_token({"sub": user.username})
    return {
        "access_token": access_token,
        "session_token": session.token,
        "token_type": "bearer"
    }

# Registro de usuario
@router.post('/register')
async def register(data: UserRequest, db: AsyncSession = Depends(get_db)):
    # Validar si el usuario ya existe
    query = select(User).where(User.username == data.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado."
        )    

    # Formatear el número de teléfono
    formatted_phone = format_phone_number(data.phone_number)

    # Crear el nuevo usuario
    new_user = User(
            username=data.username,
            hashed_password=hash_password(data.password),
            name=data.name,
            lastname=data.lastname,
            email=data.email,
            phone_number=formatted_phone  # Convertir a string antes de guardar
        )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Usuario registrado correctamente", "user_id": new_user.id}


# Endpoint para crear sesiones de usuario
@router.post("/create-session")
async def create_user_session(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Llamar a la función para crear una sesión
        new_session = await create_session(db, user_id)
        return {"session_id": new_session.id, "token": new_session.token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
