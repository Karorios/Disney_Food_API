from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated

nombre_bd = "disney_foods.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

motor = create_engine(url_bd, echo=False)

def crear_tablas(app: FastAPI):
    print("Creando tablas si no existen...")
    SQLModel.metadata.create_all(motor)
    yield
    print("Base de datos lista.")

def obtener_session() -> Session:
    with Session(motor) as session:
        yield session

SessionDep = Annotated[Session, Depends(obtener_session)]
