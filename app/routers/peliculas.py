from fastapi import APIRouter, HTTPException
from app.models import Pelicula, PeliculaCreate, PeliculaUpdate
from app.db import SessionDep

router = APIRouter(prefix="/peliculas", tags=["Películas"])


# CREATE
@router.post("/crear", response_model=Pelicula, status_code=201)
async def crear_pelicula(nueva_pelicula: PeliculaCreate, session: SessionDep):
    pelicula = Pelicula.model_validate(nueva_pelicula)
    session.add(pelicula)
    session.commit()
    session.refresh(pelicula)
    return pelicula


# FIND
@router.get("/find/all", response_model=list[Pelicula])
async def obtener_todas_las_peliculas(session: SessionDep):
    return session.query(Pelicula).all()


@router.get("/find/{pelicula_id}", response_model=Pelicula)
async def obtener_pelicula(pelicula_id: int, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula_db


# UPDATE
@router.put("/update/{pelicula_id}", response_model=Pelicula)
async def actualizar_pelicula(pelicula_id: int, datos: PeliculaUpdate, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    datos_dict = datos.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(pelicula_db, key, value)

    session.add(pelicula_db)
    session.commit()
    session.refresh(pelicula_db)
    return pelicula_db


# KILL
@router.delete("/kill/{pelicula_id}")
async def eliminar_pelicula(pelicula_id: int, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    session.delete(pelicula_db)
    session.commit()
    return {"mensaje": f"La película '{pelicula_db.titulo}' ha sido eliminada correctamente"}
