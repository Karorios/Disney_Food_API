from fastapi import APIRouter, HTTPException
from app.models import Pelicula, PeliculaCreate, PeliculaUpdate
from app.db import SessionDep

router = APIRouter(prefix="/peliculas", tags=["Películas"])

# CREATE
@router.post("/crear", response_model=Pelicula, status_code=201)
async def crear_pelicula(nueva_pelicula: PeliculaCreate, session: SessionDep):
    pelicula = Pelicula.model_validate(nueva_pelicula)
    pelicula.activo = True
    session.add(pelicula)
    session.commit()
    session.refresh(pelicula)
    return pelicula
# FIND (por ID)
@router.get("/find/{pelicula_id}", response_model=Pelicula)
async def obtener_pelicula(pelicula_id: int, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula_db
# Find Titulo
@router.get("/search/", response_model=list[Pelicula])
async def buscar_peliculas(q: str, session: SessionDep):

    resultados = session.query(Pelicula).filter(
        (Pelicula.titulo.ilike(f"%{q}%")) | (Pelicula.genero.ilike(f"%{q}%"))
    ).all()
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron resultados para '{q}'")
    return resultados

# Find genero
@router.get("/filter/", response_model=list[Pelicula])
async def filtrar_peliculas_por_genero(genero: str, session: SessionDep):

    peliculas = session.query(Pelicula).filter(Pelicula.genero.ilike(f"%{genero}%")).all()
    if not peliculas:
        raise HTTPException(status_code=404, detail=f"No se encontraron películas del género '{genero}'")
    return peliculas


# FIND (activas)
@router.get("/find/all", response_model=list[Pelicula])
async def obtener_todas_las_peliculas(session: SessionDep):
    return session.query(Pelicula).filter(Pelicula.activo == True).all()

# FIND (inactivas)
@router.get("/inactivas", response_model=list[Pelicula])
async def obtener_peliculas_inactivas(session: SessionDep):
    return session.query(Pelicula).filter(Pelicula.activo == False).all()


# UPDATE
@router.put("/update/{pelicula_id}", response_model=Pelicula)
async def actualizar_pelicula(pelicula_id: int, datos: PeliculaUpdate, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db or not pelicula_db.activo:
        raise HTTPException(status_code=404, detail="Película no encontrada o inactiva")

    datos_dict = datos.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(pelicula_db, key, value)

    session.add(pelicula_db)
    session.commit()
    session.refresh(pelicula_db)
    return pelicula_db

# DELETE (eliminación lógica)
@router.delete("/kill/{pelicula_id}")
async def eliminar_pelicula(pelicula_id: int, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db or not pelicula_db.activo:
        raise HTTPException(status_code=404, detail="Película no encontrada o ya eliminada")

    pelicula_db.activo = False
    session.add(pelicula_db)
    session.commit()
    return {"mensaje": f"La película '{pelicula_db.titulo}' fue movida a la papelera."}

# RESTORE
@router.put("/restore/{pelicula_id}", response_model=Pelicula)
async def restaurar_pelicula(pelicula_id: int, session: SessionDep):
    pelicula_db = session.get(Pelicula, pelicula_id)
    if not pelicula_db:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    if pelicula_db.activo:
        raise HTTPException(status_code=400, detail="La película ya está activa")

    pelicula_db.activo = True
    session.add(pelicula_db)
    session.commit()
    session.refresh(pelicula_db)
    return pelicula_db
