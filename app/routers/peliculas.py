from fastapi import APIRouter, HTTPException
from app.models import Pelicula, PeliculaCreate, PeliculaUpdate

router = APIRouter(prefix="/peliculas", tags=["Películas"])

peliculas_db = []
next_id = 1


@router.post("/crear", response_model=Pelicula, status_code=201)
async def crear_pelicula(nueva: PeliculaCreate):
    global next_id
    pelicula = Pelicula(id=next_id, **nueva.dict())
    next_id += 1
    peliculas_db.append(pelicula)
    return pelicula


@router.get("/find/all", response_model=list[Pelicula])
async def listar_peliculas():
    return [p for p in peliculas_db if p.activo]


@router.get("/find/{pelicula_id}", response_model=Pelicula)
async def obtener_pelicula(pelicula_id: int):
    pelicula = next((p for p in peliculas_db if p.id == pelicula_id), None)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula


@router.get("/search")
async def buscar_peliculas(Nombre: str):
    resultados = [p for p in peliculas_db if Nombre.lower() in p.titulo.lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron películas con ese término")
    return resultados

@router.get("/filter")
async def filtrar_por_genero(genero: str):
    filtradas = [p for p in peliculas_db if p.genero.lower() == genero.lower()]
    return filtradas


@router.put("/update/{pelicula_id}", response_model=Pelicula)
async def actualizar_pelicula(pelicula_id: int, datos: PeliculaUpdate):
    pelicula = next((p for p in peliculas_db if p.id == pelicula_id), None)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(pelicula, key, value)
    return pelicula


@router.delete("/kill/{pelicula_id}")
async def eliminar_pelicula(pelicula_id: int):
    pelicula = next((p for p in peliculas_db if p.id == pelicula_id), None)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    pelicula.activo = False
    return {"mensaje": f"La película '{pelicula.titulo}' fue movida a la papelera."}


@router.get("/trash", response_model=list[Pelicula])
async def listar_papelera():
    return [p for p in peliculas_db if not p.activo]


@router.put("/restore/{pelicula_id}")
async def restaurar_pelicula(pelicula_id: int):
    pelicula = next((p for p in peliculas_db if p.id == pelicula_id and not p.activo), None)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada o ya activa")
    pelicula.activo = True
    return {"mensaje": f"La película '{pelicula.titulo}' ha sido restaurada."}
