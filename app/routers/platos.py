from fastapi import APIRouter, HTTPException
from app.models import Plato, PlatoCreate, PlatoUpdate, Pelicula
from app.db import SessionDep

router = APIRouter(prefix="/platos", tags=["Platos"])

# CREATE
@router.post("/crear", response_model=Plato, status_code=201)
async def crear_plato(nuevo_plato: PlatoCreate, session: SessionDep):
    datos_plato = nuevo_plato.model_dump()
    pelicula_db = session.get(Pelicula, datos_plato.get("pelicula_id"))

    if not pelicula_db or not pelicula_db.activo:
        raise HTTPException(status_code=404, detail="Película no encontrada o inactiva")

    plato = Plato.model_validate(datos_plato)
    plato.activo = True
    session.add(plato)
    session.commit()
    session.refresh(plato)
    return plato

# FIND (por ID)
@router.get("/find/{plato_id}", response_model=Plato)
async def obtener_plato(plato_id: int, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return plato_db
# Find tipo de plato
@router.get("/filter/", response_model=list[Plato])
async def filtrar_platos_por_tipo(tipo: str, session: SessionDep):
    platos = session.query(Plato).filter(Plato.tipo.ilike(f"%{tipo}%")).all()
    if not platos:
        raise HTTPException(status_code=404, detail=f"No se encontraron platos del tipo '{tipo}'")
    return platos


# Find general
@router.get("/search/", response_model=list[Plato])
async def buscar_platos(q: str, session: SessionDep):
    resultados = session.query(Plato).filter(
        (Plato.nombre.ilike(f"%{q}%")) | (Plato.descripcion.ilike(f"%{q}%"))
    ).all()
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron resultados para '{q}'")
    return resultados


# FIND (activos)
@router.get("/find/all", response_model=list[Plato])
async def obtener_todos_los_platos(session: SessionDep):
    return session.query(Plato).filter(Plato.activo == True).all()

# FIND (inactivos)
@router.get("/inactivos", response_model=list[Plato])
async def obtener_platos_inactivos(session: SessionDep):
    return session.query(Plato).filter(Plato.activo == False).all()


# UPDATE
@router.put("/update/{plato_id}", response_model=Plato)
async def actualizar_plato(plato_id: int, datos: PlatoUpdate, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db or not plato_db.activo:
        raise HTTPException(status_code=404, detail="Plato no encontrado o inactivo")

    datos_dict = datos.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(plato_db, key, value)

    session.add(plato_db)
    session.commit()
    session.refresh(plato_db)
    return plato_db

# DELETE
@router.delete("/kill/{plato_id}")
async def eliminar_plato(plato_id: int, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db or not plato_db.activo:
        raise HTTPException(status_code=404, detail="Plato no encontrado o ya inactivo")

    plato_db.activo = False
    session.add(plato_db)
    session.commit()
    return {"mensaje": f"El plato '{plato_db.nombre}' fue movido a la papelera."}

# RESTORE
@router.put("/restore/{plato_id}", response_model=Plato)
async def restaurar_plato(plato_id: int, session: SessionDep):
    plato_db = session.get(Plato, plato_id)
    if not plato_db:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    if plato_db.activo:
        raise HTTPException(status_code=400, detail="El plato ya está activo")

    plato_db.activo = True
    session.add(plato_db)
    session.commit()
    session.refresh(plato_db)
    return plato_db
