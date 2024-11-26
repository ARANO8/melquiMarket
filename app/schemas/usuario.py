# app/schemas/usuario.py

from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str  # Contraseña requerida al crear un nuevo usuario
    avatar: str | None = None  # Avatar opcional

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    avatar: str | None = None  # Permitir actualización opcional del avatar

class Usuario(UsuarioBase):
    idUsuario: int
    avatar: str | None = None  # Incluir avatar en la respuesta del usuario
    password: str | None = None  # Incluir password para mostrar el hash en la respuesta

    class Config:
        from_attributes = True
