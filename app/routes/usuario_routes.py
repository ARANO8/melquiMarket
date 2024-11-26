# app/routes/usuario_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.controllers.usuario_controller import (
    actualizar_usuario,
    create_usuario,
    eliminar_usuario,
    get_usuarios,
    get_usuario
)
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, Usuario  # Asegúrate de que UsuarioUpdate esté importado
from app.utils.auth import get_current_user, get_current_admin  # Importa la función para obtener el usuario actual y el admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Endpoint para hacer creacion del primer usuario
# @router.post("/usuarios/", response_model=Usuario)
# def create_new_usuario(
#     usuario: UsuarioCreate, 
#     db: Session = Depends(get_db)
# ):
#     # Esto solo aplica mientras creamos el primer administrador
#     # db_usuario = create_usuario(db=db, usuario=usuario)
#     return create_usuario(db=db, usuario=usuario)


# Endpoint para crear un nuevo usuario (solo administradores)
@router.post("/usuarios/", response_model=Usuario)
def create_new_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_admin)  # Solo el administrador puede crear usuarios
):
    db_usuario = create_usuario(db=db, usuario=usuario)
    return db_usuario


# Endpoint para obtener todos los usuarios (solo administradores)
@router.get("/usuarios/", response_model=list[Usuario])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    usuarios = get_usuarios(db, skip=skip, limit=limit)
    return usuarios


# Endpoint para obtener un usuario específico por ID (solo administradores)
@router.get("/usuarios/{user_id}", response_model=Usuario)
def read_usuario(user_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_usuario = get_usuario(db, user_id=user_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


# Endpoint para actualizar un usuario (solo el propio usuario o un administrador)
@router.put("/usuarios/{usuario_id}/editar", response_model=Usuario)
def editar_usuario(usuario_id: int, usuario_actualizado: UsuarioUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # Asegurarse de que solo el propio usuario o un administrador pueda actualizar los datos
    if current_user.rol != "administrador" and current_user.idUsuario != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este usuario")
    
    usuario = actualizar_usuario(db=db, usuario_id=usuario_id, usuario_actualizado=usuario_actualizado)
    return usuario

# Endpoint para eliminar un usuario (solo administradores)
@router.delete("/usuarios/{usuario_id}/eliminar", response_model=dict)
def eliminar_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    return eliminar_usuario(db=db, usuario_id=usuario_id)
