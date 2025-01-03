from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta
from app.models import User, Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.database import get_db


SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 60   # Duración token en minutos

def create_access_token(data: dict) -> str:  # Genera token y tiempo expiración
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) 
    return token

# Función para hashear contraseñas
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


async def authenticate_user(db: AsyncSession, username: str, password: str):
    # Buscar al usuario en la base de datos
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None or not verify_password(password, user.hashed_password):  # Usa bcrypt para verificar
        return None
    return user

# Función para crear el token de acceso y guardarlo en la base de datos
async def create_session(db: AsyncSession, user_id: int):
    query = select(Session).where(Session.user_id == user_id, Session.expires_at > datetime.utcnow())
    result = await db.execute(query)
    active_session = result.scalar_one_or_none()

    if active_session:
        return active_session  # Devolver la sesión activa existente
    
    # Crear el token de acceso
    access_token = create_access_token({"sub": user_id})

    # Calcular la fecha de expiración
    expires_at = datetime.utcnow() + timedelta(hours=1)

    # Crear una nueva sesión
    new_session = Session(
        user_id=user_id,
        token=access_token,
        expires_at=expires_at
    )

    # Guardar la sesión en la base de datos
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return new_session

# Función para verificar si el token está en la base de datos y si ha expirado
async def verify_token_in_db(token: str, db: AsyncSession):
    # Verificar si el token existe en la base de datos
    query = select(Session).where(Session.token == token)
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no válido")

    # Verificar si el token ha expirado
    if session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")

    return session