from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import Base, engine
from app.routes.auth_routes import router as auth_router 
from app.routes.usuario_routes import router as usuario_router
from app.routes.producto_routes import router as producto_router
from app.routes.categoria_routes import router as categoria_router

app = FastAPI()

# Montar los archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir los routers de autenticación, usuarios, productos, y categorías
app.include_router(auth_router, prefix="/api/v1", tags=["Autenticación"])
app.include_router(usuario_router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(producto_router, prefix="/api/v1", tags=["Productos"])
app.include_router(categoria_router, prefix="/api/v1", tags=["Categorías"])

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)
