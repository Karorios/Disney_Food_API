from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "postgresql+psycopg2://u5hyh5mb6dtuaxyhpy9c:DF57wKULBw1qJxyUZ1hwoWraANL6A6@buc5spn0v3jtzw9pjmkx-postgresql.services.clever-cloud.com:50013/buc5spn0v3jtzw9pjmkx"

engine = create_engine(DATABASE_URL, echo=True)

def crear_tablas():
    print("Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("Tablas listas")

def obtener_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(obtener_session)]
