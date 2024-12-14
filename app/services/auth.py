import jwt
import bcrypt
from datetime import datetime, timedelta
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


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