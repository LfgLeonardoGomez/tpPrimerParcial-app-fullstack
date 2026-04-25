import os
from typing import Optional
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# Importar todos los modelos para que SQLModel los registre
from app.categoria.model import Categoria
from app.producto.model import Producto
from app.core.models import ProductoCategoria

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "tp3_appfullstack")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Construir URL de conexión
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Motor de base de datos
engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Obtener el motor de base de datos (singleton pattern)"""
    print("MIRA ACA !!!!!")
    print("DB_HOST:", DB_HOST)
    print("DB_NAME:", DB_NAME)
    print("DB_USER:", DB_USER)
    print("DB_PASSWORD:", DB_PASSWORD)
    print("DATABASE_URL:", DATABASE_URL)

    global engine
    if engine is None:
        engine = create_engine(
            DATABASE_URL,
            echo=os.getenv("DEBUG", "false").lower() == "true",  # Mostrar queries SQL en debug
            pool_pre_ping=True,  # Verificar conexiones antes de usarlas
            pool_recycle=3600,   # Reciclar conexiones cada hora
        )
    return engine


def create_db_and_tables():
    """Crear todas las tablas de la base de datos"""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Obtener una sesión de base de datos"""
    engine = get_engine()
    with Session(engine) as session:
        yield session


def get_session_dependency() -> Session:
    """Dependencia para FastAPI - retorna una sesión de base de datos"""
    engine = get_engine()
    with Session(engine) as session:
        yield session


# Función para cerrar conexiones (útil para testing o shutdown)
def dispose_engine():
    """Cerrar todas las conexiones del motor"""
    global engine
    if engine:
        engine.dispose()
        engine = None