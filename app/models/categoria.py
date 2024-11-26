# app/models/categoria.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base
from app.models.producto_categoria import producto_categoria  # Asegúrate de importar la tabla intermedia

class Categoria(Base):
    __tablename__ = 'categorias'

    idCategoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

    productos = relationship("Producto", secondary=producto_categoria, back_populates="categorias")
