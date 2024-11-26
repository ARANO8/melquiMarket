# app/controllers/usuario_controller.py

from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext

# Configuración para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=get_password_hash(usuario.password),
        avatar=usuario.avatar,
        rol=usuario.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.idUsuario == user_id).first()

def actualizar_usuario(db: Session, usuario_id: int, usuario_actualizado: UsuarioUpdate):
    usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar los campos solo si se proporcionan
    if usuario_actualizado.nombre is not None:
        usuario.nombre = usuario_actualizado.nombre
    if usuario_actualizado.email is not None:
        usuario.email = usuario_actualizado.email
    if usuario_actualizado.password is not None:
        usuario.password = get_password_hash(usuario_actualizado.password)
    if usuario_actualizado.avatar is not None:
        usuario.avatar = usuario_actualizado.avatar

    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"detail": "Usuario eliminado exitosamente"}
