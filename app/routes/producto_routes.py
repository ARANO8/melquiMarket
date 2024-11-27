# app/routes/producto_routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.controllers.producto_controller import (
    actualizar_producto,
    actualizar_stock_producto,
    create_producto,
    eliminar_producto,
    get_productos,
    get_producto,
    obtener_productos_bajo_stock,
    decrementar_cantidad_producto,
    reemplazar_cantidad_producto,
    obtener_historial_inventario
)
from app.controllers.categoria_controller import get_categoria
from app.schemas.producto import ProductoCreate, Producto, ProductoUpdate, ProductoUpdateAll
from app.schemas.historial_inventario import HistorialInventario as HistorialInventarioSchema
from app.models.usuario import Usuario
from app.utils.auth import get_current_admin, get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo producto (solo administradores)
@router.post("/productos/", response_model=Producto)
def create_new_producto(
    producto: ProductoCreate, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_admin)
):
    db_producto = create_producto(db=db, producto=producto)
    return db_producto

# Endpoint para obtener todos los productos
@router.get("/productos/", response_model=list[Producto])
def read_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    productos = get_productos(db, skip=skip, limit=limit)
    return productos

# Endpoint para obtener un producto específico por ID
@router.get("/productos/{producto_id}", response_model=Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_producto = get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Endpoint para actualizar un producto (solo administradores)
@router.put("/productos/{producto_id}/editar", response_model=Producto)
def editar_producto(
    producto_id: int, 
    producto_actualizado: ProductoUpdateAll, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_admin)
):
    producto = actualizar_producto(db=db, producto_id=producto_id, producto_actualizado=producto_actualizado)
    return producto

# Endpoint para eliminar un producto (solo administradores)
@router.delete("/productos/{producto_id}/eliminar", response_model=dict)
def eliminar_producto_endpoint(producto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    return eliminar_producto(db=db, producto_id=producto_id)

# Endpoint para agregar categorías a un producto
@router.post("/productos/{producto_id}/categorias/{categoria_id}", response_model=Producto)
def add_categoria_to_producto(producto_id: int, categoria_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    producto = get_producto(db=db, producto_id=producto_id)
    categoria = get_categoria(db=db, categoria_id=categoria_id)
    if producto is None or categoria is None:
        raise HTTPException(status_code=404, detail="Producto o categoría no encontrada")
    
    # Añadir la categoría al producto
    if categoria not in producto.categorias:
        producto.categorias.append(categoria)
    
    db.commit()
    db.refresh(producto)
    return producto

# Endpoint para registrar devolucion de un producto
@router.post("/devoluciones/", response_model=Producto)
def registrar_devolucion(producto_id: int, cantidad: int, db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    producto = actualizar_stock_producto(db=db, producto_id=producto_id, cantidad=cantidad, motivo=f"Devolucion realizada por {current_user.nombre} ({current_user.email})")
    return producto

# Endpoint para registrar el reabastecimiento de un producto (solo administrador)
@router.post("/reabastecimientos/", response_model=Producto)
def registrar_reabastecimiento(producto_id: int, cantidad: int, db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_admin)):
    producto = actualizar_stock_producto(db=db, producto_id=producto_id, cantidad=cantidad, motivo=f"Rebastecimiento realizada por {current_user.nombre} ({current_user.email})")
    return producto

# Endpoint para registrar una venta de un producto
@router.post("/ventas/", response_model=Producto)
def realizar_venta(producto_id: int, cantidad: int, db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    producto = decrementar_cantidad_producto(db=db, producto_id=producto_id, cantidad=cantidad, motivo=f"Venta realizada por {current_user.nombre} ({current_user.email})")
    return producto

# Endpoint para reemplazar la cantidad del producto (solo administrador)
@router.put("/productos/{producto_id}/reemplazar", response_model=Producto)
def reemplazar_cantidad(producto_id: int, cantidad: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    producto = reemplazar_cantidad_producto(db=db, producto_id=producto_id, cantidad=cantidad, motivo=f"Reemplazo de cantidad realizada por {current_user.nombre} ({current_user.email})")
    return producto

# Endpoint para obtener productos con bajo stock
@router.get("/productos/bajo-stock/alerta", response_model=list[Producto])
def productos_bajo_stock(
    nivel_alerta: int = 10,
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)
):
    if nivel_alerta is None:
        nivel_alerta = 10  # Asignamos un valor por defecto si no está presente

    productos = obtener_productos_bajo_stock(db=db, nivel_alerta=nivel_alerta)
    return productos


# Endpoint para obtener el historial de cambios de un producto específico
@router.get("/productos/{producto_id}/historial", response_model=list[HistorialInventarioSchema])
def historial_producto(producto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    historial = obtener_historial_inventario(db=db, producto_id=producto_id)
    return historial