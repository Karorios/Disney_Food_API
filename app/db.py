from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv()  # Carga el archivo .env automáticamente

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")

if not DATABASE_URL:
    raise ValueError("ERROR: No se encontró POSTGRESQL_ADDON_URI en el .env. Verifica tus variables.")


if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://")

# Crear motor de conexión
engine = create_engine(DATABASE_URL, echo=True)


def crear_tablas():
    print("🛠 Creando tablas en la base de datos de Clever Cloud…")
    SQLModel.metadata.create_all(engine)
    print("✔ Tablas creadas correctamente")


def obtener_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(obtener_session)]
