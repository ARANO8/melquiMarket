# app/controllers/producto_controller.py

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.historial_inventario import HistorialInventario
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoUpdateAll

LIMITE_REABASTECIMIENTO = 1000

# Función para crear un nuevo producto
def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        cantidad=producto.cantidad,
        estado=producto.estado,
        imagen=producto.imagen,
        nivel_alerta_stock=producto.nivel_alerta_stock
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)

    # Registrar la creación en el historial
    historial = HistorialInventario(
        idProducto=db_producto.idProducto,
        motivo="Creación de producto",
        cantidad_cambio=None,
        fecha_cambio=datetime.utcnow()
    )
    db.add(historial)
    db.commit()

    return db_producto


# Función para obtener productos
def get_productos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Producto).filter(Producto.estado == True).offset(skip).limit(limit).all()

# Función para obtener un producto por ID
def get_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.idProducto == producto_id, Producto.estado == True).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Función para actualizar un producto
def actualizar_producto(db: Session, producto_id: int, producto_actualizado: ProductoUpdateAll):
    producto = db.query(Producto).filter(Producto.idProducto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Capturar información antes del cambio
    info_anterior = producto.__dict__.copy()

    # Actualizar el producto
    producto.nombre = producto_actualizado.nombre
    producto.descripcion = producto_actualizado.descripcion
    producto.precio = producto_actualizado.precio
    producto.cantidad = producto_actualizado.cantidad
    producto.estado = producto_actualizado.estado
    producto.imagen = producto_actualizado.imagen
    producto.nivel_alerta_stock = producto_actualizado.nivel_alerta_stock

    db.commit()
    db.refresh(producto)

    # Registrar la actualización en el historial
    historial = HistorialInventario(
        idProducto=producto.idProducto,
        motivo="Actualización de producto",
        cantidad_cambio=None,
        fecha_cambio=datetime.utcnow()
    )
    historial_detalle = {
        "anterior": info_anterior,
        "actual": producto.__dict__
    }
    # Aquí podrías incluir más lógica para guardar este detalle como JSON si lo deseas.

    db.add(historial)
    db.commit()

    return producto



# Función para actualizar el stock (incrementar cantidad)
def actualizar_stock_producto(db: Session, producto_id: int, cantidad: int, motivo: str):
    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser un valor positivo.")
    
    if cantidad > LIMITE_REABASTECIMIENTO:
        raise HTTPException(status_code=400, detail=f"La cantidad máxima permitida para reabastecimiento es de {LIMITE_REABASTECIMIENTO} unidades.")

    producto = db.query(Producto).filter(Producto.idProducto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cantidad_anterior = producto.cantidad
    producto.cantidad += cantidad

    db.commit()
    db.refresh(producto)

    # Registrar en el historial
    historial = HistorialInventario(
        idProducto=producto.idProducto,
        motivo=motivo,
        cantidad_cambio=cantidad,
        cantidad_anterior=cantidad_anterior,
        cantidad_actual=producto.cantidad,
        fecha_cambio=datetime.utcnow()
    )
    db.add(historial)
    db.commit()

    return producto


# Función para decrementar la cantidad del producto
def decrementar_cantidad_producto(db: Session, producto_id: int, cantidad: int, motivo: str):
    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser un valor positivo.")
    
    producto = db.query(Producto).filter(Producto.idProducto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="Cantidad insuficiente en el inventario")
    
    cantidad_anterior = producto.cantidad
    producto.cantidad -= cantidad

    # Registrar en el historial
    historial = HistorialInventario(
        idProducto=producto.idProducto,
        motivo=motivo,
        cantidad_cambio=cantidad,
        cantidad_anterior=cantidad_anterior,
        cantidad_actual=producto.cantidad,
        fecha_cambio=datetime.utcnow()
    )
    db.add(historial)
    db.commit()
    db.refresh(producto)
    return producto

# Función para reemplazar la cantidad del producto
def reemplazar_cantidad_producto(db: Session, producto_id: int, cantidad: int, motivo: str):
    if cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser un valor positivo.")
    
    if cantidad > LIMITE_REABASTECIMIENTO:
        raise HTTPException(status_code=400, detail=f"La cantidad máxima permitida para reabastecimiento es de {LIMITE_REABASTECIMIENTO} unidades.")

    producto = db.query(Producto).filter(Producto.idProducto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cantidad_anterior = producto.cantidad
    producto.cantidad = cantidad

    # Crear una entrada en el historial del inventario
    # Registrar en el historial
    historial = HistorialInventario(
        idProducto=producto.idProducto,
        motivo=motivo,
        cantidad_cambio=cantidad,
        cantidad_anterior=cantidad_anterior,
        cantidad_actual=producto.cantidad,
        fecha_cambio=datetime.utcnow()
    )
    db.add(historial)
    db.commit()
    db.refresh(producto)
    return producto

def eliminar_producto(db: Session, producto_id: int, motivo: str):
    producto = db.query(Producto).filter(Producto.idProducto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Registrar la eliminación en el historial
    historial = HistorialInventario(
        idProducto=producto.idProducto,
        motivo= motivo,
        cantidad_cambio=None,
        fecha_cambio=datetime.utcnow()
    )
    db.add(historial)
    producto.estado = False
    db.commit()
    db.refresh(producto)
    return {"detail": "Producto eliminado exitosamente"}



# Función para obtener productos con bajo stock
def obtener_productos_bajo_stock(db: Session, nivel_alerta: int = 10):
    return db.query(Producto).filter(Producto.cantidad <= nivel_alerta).all()


# Función para obtener el historial de cambios de un producto específico
def obtener_historial_inventario(db: Session, producto_id: int):
    historial = db.query(HistorialInventario).filter(HistorialInventario.idProducto == producto_id).all()
    if not historial:
        raise HTTPException(status_code=404, detail="No hay cambios registrados para este producto")
    return historial
