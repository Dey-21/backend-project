import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import HTTPException
from app.models import User
from app.database import AsyncSession

SECRET_KEY = "secret"
ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE = 60   # Duración token en minutos

def create_access_token(data: dict, token_expire: int):    # Genera token y tiempo expiración
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=token_expire)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) 


def get_password_hash(password: str):
    return generate_password_hash(password)  


def verify_password(plain_password: str, hashed_password: str):
    return check_password_hash(hashed_password, password)


async def add_user(db: AsyncSession, username: str, password: str):
  hashed_password = get_password_hash(password)
  user = User(username=username, hashed_password=hashed_password)    
 
  try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return {"message": "User created successfully", "user_id": user.id}
  #Integrity error
  except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Data write error: {str(e)}")
  # SQLAlchemy General Error
  except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")  


async def get_user_by_name(db: AsyncSession, username: str):
    return await db.query(User).filter(User.username == username).first()


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = get_user_by_name(db, username)
    if user is None:
        return {"message": f"The user {username} is not registered in the system"}
    
    if verify_password(user.password, password):
        return create_access_token({'user_id': user.id}, 60)
    
    return {"message": "Invalid user password"}
