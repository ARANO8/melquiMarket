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

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo producto
@router.post("/productos/", response_model=Producto)
def create_new_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = create_producto(db=db, producto=producto)
    return db_producto

# Endpoint para obtener todos los productos
@router.get("/productos/", response_model=list[Producto])
def read_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    productos = get_productos(db, skip=skip, limit=limit)
    return productos

# Endpoint para obtener un producto específico por ID
@router.get("/productos/{producto_id}", response_model=Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Endpoint para actualizar un producto
@router.put("/productos/{producto_id}/editar", response_model=Producto)
def editar_producto(producto_id: int, producto_actualizado: ProductoUpdateAll, db: Session = Depends(get_db)):
    producto = actualizar_producto(db=db, producto_id=producto_id, producto_actualizado=producto_actualizado)
    return producto

# Endpoint para eliminar un producto
@router.delete("/productos/{producto_id}/eliminar", response_model=dict)
def eliminar_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    return eliminar_producto(db=db, producto_id=producto_id)

# Endpoint para agregar categorías a un producto
@router.post("/productos/{producto_id}/categorias/{categoria_id}", response_model=Producto)
def add_categoria_to_producto(producto_id: int, categoria_id: int, db: Session = Depends(get_db)):
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

# Endpoint para incrementar la cantidad del producto
@router.put("/productos/{producto_id}/incrementar", response_model=Producto)
def incrementar_cantidad(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    producto = actualizar_stock_producto(db=db, producto_id=producto_id, cantidad=cantidad, motivo="Incremento de stock")
    return producto

# Endpoint para decrementar la cantidad del producto
@router.put("/productos/{producto_id}/decrementar", response_model=Producto)
def decrementar_cantidad(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    producto = decrementar_cantidad_producto(db=db, producto_id=producto_id, cantidad=cantidad)
    return producto

# Endpoint para reemplazar la cantidad del producto
@router.put("/productos/{producto_id}/reemplazar", response_model=Producto)
def reemplazar_cantidad(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    producto = reemplazar_cantidad_producto(db=db, producto_id=producto_id, cantidad=cantidad)
    return producto

# Endpoint para obtener productos con bajo stock
@router.get("/productos/bajo-stock/alerta", response_model=list[Producto])
def productos_bajo_stock(
    nivel_alerta: int = 10,
    db: Session = Depends(get_db)
):
    if nivel_alerta is None:
        nivel_alerta = 10  # Asignamos un valor por defecto si no está presente

    productos = obtener_productos_bajo_stock(db=db, nivel_alerta=nivel_alerta)
    return productos


# Endpoint para obtener el historial de cambios de un producto específico
@router.get("/productos/{producto_id}/historial", response_model=list[HistorialInventarioSchema])
def historial_producto(producto_id: int, db: Session = Depends(get_db)):
    historial = obtener_historial_inventario(db=db, producto_id=producto_id)
    return historial