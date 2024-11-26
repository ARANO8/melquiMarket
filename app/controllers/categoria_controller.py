# app/controllers/categoria_controller.py

from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaBase, CategoriaCreate

def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(
        nombre=categoria.nombre,
        descripcion=categoria.descripcion
    )
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categorias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Categoria).offset(skip).limit(limit).all()

def get_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.idCategoria == categoria_id).first()


def actualizar_categoria(db: Session, categoria_id: int, categoria_actualizada: CategoriaBase):
    categoria = db.query(Categoria).filter(Categoria.idCategoria == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Actualizar los campos de la categoría
    categoria.nombre = categoria_actualizada.nombre
    categoria.descripcion = categoria_actualizada.descripcion
    db.commit()
    db.refresh(categoria)
    return categoria

def eliminar_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).filter(Categoria.idCategoria == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()
    return {"detail": "Categoría eliminada exitosamente"}