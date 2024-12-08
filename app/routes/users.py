from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter()

@router.get("/test-db")
def test_db(session: Session = Depends(SessionLocal)):
    return {"message": "Database connected successfully!"}
