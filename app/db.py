import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")

# Si no existe, intenta usar SUPABASE
if not DATABASE_URL:
    DATABASE_URL = os.getenv("SUPABASE_DB_URL")

# Si tampoco existe, usa sqlite local
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./local.db"

# Reparar formato postgres:// → postgresql+psycopg2://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://")

engine = create_engine(DATABASE_URL, echo=False)

def crear_tablas():
    print("Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("Tablas listas ✔")

def obtener_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(obtener_session)]
