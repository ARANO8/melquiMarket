# app/models/historial_inventario.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config import Base
from datetime import datetime

class HistorialInventario(Base):
    __tablename__ = "historial_inventario"

    idHistorial = Column(Integer, primary_key=True, index=True)
    idProducto = Column(Integer, ForeignKey("productos.idProducto"), nullable=False)
    motivo = Column(String, nullable=False)
    cantidad_cambio = Column(Integer, nullable=True)
    cantidad_anterior = Column(Integer, nullable=True)
    cantidad_actual = Column(Integer, nullable=True)
    fecha_cambio = Column(DateTime, default=datetime.utcnow)

    # Agregar la relación con Producto
    producto = relationship("Producto", back_populates="historial")
