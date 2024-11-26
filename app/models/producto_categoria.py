# app/models/producto_categoria.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.config import Base

producto_categoria = Table(
    'producto_categoria', Base.metadata,
    Column('idProducto', Integer, ForeignKey('productos.idProducto'), primary_key=True),
    Column('idCategoria', Integer, ForeignKey('categorias.idCategoria'), primary_key=True)
)
