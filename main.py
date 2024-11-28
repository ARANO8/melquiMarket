from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import Base, engine
from app.routes.auth_routes import router as auth_router 
from app.routes.usuario_routes import router as usuario_router
from app.routes.producto_routes import router as producto_router
from app.routes.categoria_routes import router as categoria_router
from app.routes.views_routes import router as views_router  # Importar el enrutador de vistas

app = FastAPI()

# Montar los archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir los routers de autenticación, usuarios, productos, categorías y vistas
app.include_router(auth_router, prefix="/api/v1", tags=["Autenticación"])
app.include_router(usuario_router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(producto_router, prefix="/api/v1", tags=["Productos"])
app.include_router(categoria_router, prefix="/api/v1", tags=["Categorías"])
app.include_router(views_router, tags=["Vistas"])  # Incluir el router de vistas sin prefijo

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)
