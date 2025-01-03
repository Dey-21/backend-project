from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True, nullable=False) # Campo obligatorio y único
    hashed_password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)  # Campo obligatorio y único
    phone_number = Column(String(100), unique=True, nullable=False) # Campo obligatorio y único

    # Relación con Session
    sessions = relationship("Session", back_populates="user")
    

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True)
    expires_at = Column(DateTime, nullable=False)  # Fecha de expiración del token

     # Relación con el modelo User (si deseas acceder al usuario directamente)
    user = relationship("User", back_populates="sessions")