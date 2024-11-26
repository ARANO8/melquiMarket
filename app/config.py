# app/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./melquimarket.db"

# Configurar la conexión a la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarativa base para los modelos
Base = declarative_base()
