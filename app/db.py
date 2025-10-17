from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated

nombre_bd = "disney_foods.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

motor = create_engine(
    url_bd,
    echo=False,            # Cambia a True si quieres ver las consultas SQL en consola
    connect_args={"check_same_thread": False}  # Necesario para SQLite + FastAPI
)


def crear_tablas():
    print("Creando tablas si no existen...")
    SQLModel.metadata.create_all(motor)
    print("Tablas listas.")



def obtener_sesion() -> Session:
    with Session(motor) as session:
        yield session

SessionDep = Annotated[Session, Depends(obtener_sesion)]
