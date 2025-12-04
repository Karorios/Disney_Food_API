import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

# Construcción de PostgreSQL URL desde variables de entorno
# Si no están definidas, usa SQLite como fallback para desarrollo
CLEVER_USER = os.getenv("CLEVER_USER")
CLEVER_PASSWORD = os.getenv("CLEVER_PASSWORD")
CLEVER_HOST = os.getenv("CLEVER_HOST")
CLEVER_PORT = os.getenv("CLEVER_PORT", "5432")
CLEVER_DATABASE = os.getenv("CLEVER_DATABASE")

if all([CLEVER_USER, CLEVER_PASSWORD, CLEVER_HOST, CLEVER_DATABASE]):
    DATABASE_URL = (
        f"postgresql+psycopg2://{CLEVER_USER}:"
        f"{CLEVER_PASSWORD}@"
        f"{CLEVER_HOST}:"
        f"{CLEVER_PORT}/"
        f"{CLEVER_DATABASE}"
    )
    print(f"✅ Usando PostgreSQL: {CLEVER_HOST}:{CLEVER_PORT}/{CLEVER_DATABASE}")
else:
    # Fallback a SQLite para desarrollo local
    DATABASE_URL = "sqlite:///./disney_foods.sqlite3"
    print("⚠️  Usando SQLite (fallback). Configura variables de entorno para PostgreSQL.")

print("🔍 DATABASE_URL configurado")

# Engine de SQLModel con configuración optimizada para PostgreSQL
# pool_pre_ping: Verifica conexiones antes de usarlas (útil para Render)
# pool_recycle: Recicla conexiones después de 3600 segundos
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=3600,   # Recicla conexiones cada hora
    connect_args={"connect_timeout": 10} if "postgresql" in DATABASE_URL else {}
)

# Dependencia para FastAPI (SQLModel Session)
def obtener_session():
    with Session(engine) as session:
        yield session

# Esto lo usan tus routers
SessionDep = Annotated[Session, Depends(obtener_session)]

# Crear tablas usando SQLModel
def crear_tablas():
    print("📦 Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("✔ Tablas creadas correctamente")
