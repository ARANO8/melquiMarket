# app/models/usuario.py

from sqlalchemy import Column, Integer, String
from app.config import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    idUsuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    avatar = Column(String)  # URL o Path de la imagen del usuario
    rol = Column(String, default="vendedor")
