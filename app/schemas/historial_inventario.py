# app/schemas/historial_inventario.py

from pydantic import BaseModel
from datetime import datetime

class HistorialInventarioBase(BaseModel):
    idProducto: int
    motivo: str
    cantidad_cambio: int | None = None
    cantidad_anterior: int | None = None
    cantidad_actual: int | None = None
    fecha_cambio: datetime

    class Config:
        orm_mode = True

class HistorialInventarioCreate(HistorialInventarioBase):
    pass

class HistorialInventario(HistorialInventarioBase):
    idHistorial: int
