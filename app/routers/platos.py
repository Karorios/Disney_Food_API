from fastapi import APIRouter, HTTPException
from app.models import Plato, PlatoCreate, PlatoUpdate, Pelicula
from app.db import SessionDep

router = APIRouter(prefix="/platos", tags=["Platos"])


# CREATE
@router.post("/crear", response_model=Plato, status_code=201)
async def crear_plato(nuevo_plato: PlatoCreate, session: SessionDep):
    datos_plato = nuevo_plato.model_dump()
    pelicula_db = session.get(Pelicula, datos_plato.get("pelicula_id"))

    if not pelicula_db:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    plato = Plato.model_validate(datos_plato)
    session.add(plato)
    session.commit()
    session.refresh(plato)
    return plato


# FIND
@router.get("/find/all", response_model=list[Plato])
async def obtener_todos_los_platos(session: SessionDep):
    return session.query(Plato).all()


@router.get("/find/{plato_id}", response_model=Plato)
async def obtener_plato(plato_id: int, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return plato_db


# UPDATE
@router.put("/update/{plato_id}", response_model=Plato)
async def actualizar_plato(plato_id: int, datos: PlatoUpdate, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db:
        raise HTTPException(status_code=404, detail="Plato no encontrado")

    datos_dict = datos.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(plato_db, key, value)

    session.add(plato_db)
    session.commit()
    session.refresh(plato_db)
    return plato_db


#  KILL
@router.delete("/kill/{plato_id}")
async def eliminar_plato(plato_id: int, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db:
        raise HTTPException(status_code=404, detail="Plato no encontrado")

    session.delete(plato_db)
    session.commit()
    return {"mensaje": f"El plato '{plato_db.nombre}' ha sido eliminado correctamente"}
