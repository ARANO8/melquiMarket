# app/schemas/categoria.py

from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    idCategoria: int

    class Config:
        from_attributes = True
