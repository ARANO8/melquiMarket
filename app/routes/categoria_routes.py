# app/routes/categoria_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.controllers.categoria_controller import actualizar_categoria, create_categoria, eliminar_categoria, get_categorias, get_categoria
from app.schemas.categoria import CategoriaBase, CategoriaCreate, Categoria
from app.models.usuario import Usuario
from app.utils.auth import get_current_admin, get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva categoría
@router.post("/categorias/", response_model=Categoria)
def create_new_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_admin)):
    db_categoria = create_categoria(db=db, categoria=categoria)
    return db_categoria

# Endpoint para obtener todas las categorías
@router.get("/categorias/", response_model=list[Categoria])
def read_categorias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    categorias = get_categorias(db, skip=skip, limit=limit)
    return categorias

# Endpoint para obtener una categoría específica por ID
@router.get("/categorias/{categoria_id}", response_model=Categoria)
def read_categoria(categoria_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_categoria = get_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria


# Endpoint para actualizar una categoría
@router.put("/categorias/{categoria_id}/editar", response_model=CategoriaBase)
def editar_categoria(categoria_id: int, categoria_actualizada: CategoriaBase, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    categoria = actualizar_categoria(db=db, categoria_id=categoria_id, categoria_actualizada=categoria_actualizada)
    return categoria

# Endpoint para eliminar una categoría
@router.delete("/categorias/{categoria_id}/eliminar", response_model=dict)
def eliminar_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    return eliminar_categoria(db=db, categoria_id=categoria_id)