from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import SessionDep
from app.models import Pelicula, PeliculaCreate, PeliculaUpdate

router = APIRouter(prefix="/peliculas", tags=["Películas"])


# -----------------------------
# Crear película
# -----------------------------
@router.post("/crear", response_model=Pelicula, status_code=201)
def crear_pelicula(
    nueva: PeliculaCreate,
    session: SessionDep
):
    try:
        print(f"📝 Intentando crear película: {nueva.titulo}")
        pelicula = Pelicula(**nueva.model_dump())
        session.add(pelicula)
        session.commit()
        session.refresh(pelicula)
        print(f"✅ Película creada exitosamente con ID: {pelicula.id}")
        return pelicula
    except Exception as e:
        session.rollback()
        print(f"❌ Error al crear película: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al crear película: {str(e)}")


# -----------------------------
# Listar todas las películas activas
# -----------------------------
@router.get("/find/all", response_model=list[Pelicula])
def listar_peliculas(session: SessionDep):
    peliculas = session.exec(
        select(Pelicula).where(Pelicula.activo == True)
    ).all()
    return peliculas


# -----------------------------
# Obtener una película por ID
# -----------------------------
@router.get("/find/{pelicula_id}", response_model=Pelicula)
def obtener_pelicula(pelicula_id: int, session: SessionDep):
    pelicula = session.get(Pelicula, pelicula_id)
    if not pelicula or not pelicula.activo:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula


# -----------------------------
# Buscar película por nombre
# -----------------------------
@router.get("/search", response_model=list[Pelicula])
def buscar_peliculas(session: SessionDep, nombre: str = Query(..., description="Término de búsqueda")):
    stmt = select(Pelicula).where(
        Pelicula.titulo.ilike(f"%{nombre}%"),
        Pelicula.activo == True
    )
    resultados = session.exec(stmt).all()

    if not resultados:
        return []  # Retornar lista vacía en lugar de error 404

    return resultados


# -----------------------------
# Filtrar por género
# -----------------------------
@router.get("/filter", response_model=list[Pelicula])
def filtrar_por_genero(
    session: SessionDep,
    genero: str = Query(..., description="Filtrar por género")
):
    filtradas = session.exec(
        select(Pelicula).where(Pelicula.genero.ilike(f"%{genero}%"), Pelicula.activo == True)
    ).all()
    return filtradas


# -----------------------------
# Actualizar película
# -----------------------------
@router.put("/update/{pelicula_id}", response_model=Pelicula)
def actualizar_pelicula(
    pelicula_id: int,
    datos: PeliculaUpdate,
    session: SessionDep
):
    pelicula = session.get(Pelicula, pelicula_id)

    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(pelicula, key, value)

    session.add(pelicula)
    session.commit()
    session.refresh(pelicula)

    return pelicula


# -----------------------------
# Eliminar (mover a papelera)
# -----------------------------
@router.delete("/kill/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int, session: SessionDep):
    pelicula = session.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    pelicula.activo = False
    session.add(pelicula)
    session.commit()

    return {"mensaje": f"La película '{pelicula.titulo}' fue movida a la papelera."}


# -----------------------------
# Ver papelera
# -----------------------------
@router.get("/trash", response_model=list[Pelicula])
def listar_papelera(session: SessionDep):
    papelera = session.exec(
        select(Pelicula).where(Pelicula.activo == False)
    ).all()
    return papelera


# -----------------------------
# Restaurar película eliminada
# -----------------------------
@router.put("/restore/{pelicula_id}")
def restaurar_pelicula(pelicula_id: int, session: SessionDep):
    pelicula = session.get(Pelicula, pelicula_id)

    if not pelicula or pelicula.activo:
        raise HTTPException(status_code=404, detail="Película no encontrada o ya activa")

    pelicula.activo = True
    session.add(pelicula)
    session.commit()

    return {"mensaje": f"La película '{pelicula.titulo}' ha sido restaurada."}
