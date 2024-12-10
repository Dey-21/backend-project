from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text  # Importar la función text
from app.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/test-connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        # Usar text para la consulta SQL
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database connection is working!"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}
