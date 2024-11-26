# app/schemas/producto.py

from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    estado: str
    imagen: str | None = None
    nivel_alerta_stock: int

    class Config:
        orm_mode = True  # Cambia 'from_attributes' a 'orm_mode'

class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    cantidad: int
    nivel_alerta_stock: int | None = None  # Permitir actualización opcional de nivel_alerta_stock
    
class ProductoUpdateAll(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    estado: str
    imagen: str | None = None
    nivel_alerta_stock: int

class Producto(ProductoBase):
    idProducto: int

    class Config:
        orm_mode = True  # Cambia 'from_attributes' a 'orm_mode'
