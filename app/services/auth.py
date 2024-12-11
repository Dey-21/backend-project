from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import HTTPException
from app.models import User
from app.database import AsyncSession


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
