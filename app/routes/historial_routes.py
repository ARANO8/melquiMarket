# app/routes/historial_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.historial_inventario import HistorialInventario

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener el historial del inventario
@router.get("/historial/", response_model=list[HistorialInventario])
def obtener_historial(db: Session = Depends(get_db)):
    return db.query(HistorialInventario).all()
