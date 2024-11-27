# app/models/producto.py

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.config import Base
from app.models.producto_categoria import producto_categoria

class Producto(Base):
    __tablename__ = 'productos'

    idProducto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    cantidad = Column(Integer)
    estado = Column(Boolean, default=True)
    imagen = Column(String)
    nivel_alerta_stock = Column(Integer)

    categorias = relationship("Categoria", secondary=producto_categoria, back_populates="productos")

    # Agregar la relación con el historial de inventario
    historial = relationship("HistorialInventario", back_populates="producto", cascade="all, delete")
