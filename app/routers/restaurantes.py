from fastapi import APIRouter, HTTPException
from app.models import Restaurante, RestauranteCreate, RestauranteUpdate
from app.db import SessionDep

router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])


# CREATE
@router.post("/crear", response_model=Restaurante, status_code=201)
async def crear_restaurante(nuevo_restaurante: RestauranteCreate, session: SessionDep):
    restaurante = Restaurante.model_validate(nuevo_restaurante)
    session.add(restaurante)
    session.commit()
    session.refresh(restaurante)
    return restaurante


# ✅ FIND ALL (solo activos)
@router.get("/find/all", response_model=list[Restaurante])
async def obtener_todos_restaurantes(session: SessionDep):
    return session.query(Restaurante).filter(Restaurante.activo == True).all()


# FIND ONE (por ID)
@router.get("/find/{restaurante_id}", response_model=Restaurante)
async def obtener_restaurante(restaurante_id: int, session: SessionDep):
    restaurante_db = session.get(Restaurante, restaurante_id)
    if not restaurante_db or not restaurante_db.activo:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado o inactivo")
    return restaurante_db


# FIND INACTIVOS
@router.get("/inactivos", response_model=list[Restaurante])
async def obtener_restaurantes_inactivos(session: SessionDep):
    return session.query(Restaurante).filter(Restaurante.activo == False).all()


# UPDATE
@router.put("/update/{restaurante_id}", response_model=Restaurante)
async def actualizar_restaurante(restaurante_id: int, datos: RestauranteUpdate, session: SessionDep):
    restaurante_db = session.get(Restaurante, restaurante_id)
    if not restaurante_db or not restaurante_db.activo:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado o inactivo")

    datos_dict = datos.model_dump(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(restaurante_db, key, value)

    session.add(restaurante_db)
    session.commit()
    session.refresh(restaurante_db)
    return restaurante_db


# DELETE
@router.delete("/kill/{restaurante_id}")
async def eliminar_restaurante(restaurante_id: int, session: SessionDep):
    restaurante_db = session.get(Restaurante, restaurante_id)
    if not restaurante_db or not restaurante_db.activo:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado o ya inactivo")

    restaurante_db.activo = False
    session.add(restaurante_db)
    session.commit()
    return {"mensaje": f"El restaurante '{restaurante_db.nombre}' ha sido movido a la papelera."}


# RESTORE
@router.put("/restore/{restaurante_id}")
async def restaurar_restaurante(restaurante_id: int, session: SessionDep):
    restaurante_db = session.get(Restaurante, restaurante_id)
    if not restaurante_db:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    if restaurante_db.activo:
        raise HTTPException(status_code=400, detail="El restaurante ya está activo")

    restaurante_db.activo = True
    session.add(restaurante_db)
    session.commit()
    return {"mensaje": f"El restaurante '{restaurante_db.nombre}' ha sido restaurado correctamente."}
