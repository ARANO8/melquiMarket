# app/schemas/usuario.py

from pydantic import BaseModel, EmailStr
from enum import Enum

class RolEnum(str, Enum):
    administrador = "administrador"
    vendedor = "vendedor"

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str  # Contraseña requerida al crear un nuevo usuario
    avatar: str | None = None  # Avatar opcional
    rol: RolEnum
    
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    avatar: str | None = None  # Permitir actualización opcional del avatar
    rol: RolEnum | None = None

class Usuario(UsuarioBase):
    idUsuario: int
    avatar: str | None = None  # Incluir avatar en la respuesta del usuario
    password: str | None = None  # Incluir password para mostrar el hash en la respuesta
    rol: RolEnum

    class Config:
        from_attributes = True
