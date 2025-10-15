from fastapi import APIRouter, HTTPException
from app.models import Receta, RecetaCreate, RecetaUpdate, Plato
from app.db import SessionDep

router = APIRouter(prefix="/recetas", tags=["Recetas"])


# CREATE
@router.post("/crear", response_model=Receta, status_code=201)
async def crear_receta(nueva_receta: RecetaCreate, session: SessionDep):
    datos_receta = nueva_receta.model_dump()
    plato_db = session.get(Plato, datos_receta.get("plato_id"))
    if not plato_db or not plato_db.activo:
        raise HTTPException(status_code=404, detail="Plato no encontrado o inactivo")

    receta = Receta.model_validate(datos_receta)
    session.add(receta)
    session.commit()
    session.refresh(receta)
    return receta


# FIND ALL (solo activas)
@router.get("/find/all", response_model=list[Receta])
async def obtener_todas_recetas(session: SessionDep):
    return session.query(Receta).filter(Receta.activo == True).all()


# FIND ONE (por ID)
@router.get("/find/{receta_id}", response_model=Receta)
async def obtener_receta(receta_id: int, session: SessionDep):
    receta_db = session.get(Receta, receta_id)
    if not receta_db or not receta_db.activo:
        raise HTTPException(status_code=404, detail="Receta no encontrada o inactiva")
    return receta_db


# FIND INACTIVOS (papelera)
@router.get("/inactivos", response_model=list[Receta])
async def obtener_recetas_inactivas(session: SessionDep):
    return session.query(Receta).filter(Receta.activo == False).all()


# UPDATE
@router.put("/update/{receta_id}", response_model=Receta)
async def actualizar_receta(receta_id: int, datos: RecetaUpdate, session: SessionDep):
    receta_db = session.get(Receta, receta_id)
    if not receta_db or not receta_db.activo:
        raise HTTPException(status_code=404, detail="Receta no encontrada o inactiva")

    datos_dict = datos.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(receta_db, key, value)

    session.add(receta_db)
    session.commit()
    session.refresh(receta_db)
    return receta_db


# DELETE
@router.delete("/kill/{receta_id}")
async def eliminar_receta(receta_id: int, session: SessionDep):
    receta_db = session.get(Receta, receta_id)
    if not receta_db or not receta_db.activo:
        raise HTTPException(status_code=404, detail="Receta no encontrada o ya inactiva")

    receta_db.activo = False
    session.add(receta_db)
    session.commit()
    return {"mensaje": f"La receta '{receta_db.nombre}' ha sido movida a la papelera."}


# RESTORE
@router.put("/restore/{receta_id}")
async def restaurar_receta(receta_id: int, session: SessionDep):
    receta_db = session.get(Receta, receta_id)
    if not receta_db:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    if receta_db.activo:
        raise HTTPException(status_code=400, detail="La receta ya está activa")

    receta_db.activo = True
    session.add(receta_db)
    session.commit()
    return {"mensaje": f"La receta '{receta_db.nombre}' ha sido restaurada correctamente."}
