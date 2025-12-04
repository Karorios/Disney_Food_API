from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import SessionDep
from app.models import Receta, RecetaCreate, RecetaUpdate

router = APIRouter(prefix="/recetas", tags=["Recetas"])


@router.post("/crear", response_model=Receta, status_code=201)
async def crear_receta(data: RecetaCreate, session: SessionDep):
    nueva = Receta(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


@router.get("/find/all", response_model=list[Receta])
async def listar_recetas(session: SessionDep):
    return session.exec(select(Receta).where(Receta.activo == True)).all()


@router.get("/find/{receta_id}", response_model=Receta)
async def obtener_receta(receta_id: int, session: SessionDep):
    receta = session.get(Receta, receta_id)
    if not receta or not receta.activo:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta


@router.get("/search", response_model=list[Receta])
async def buscar_recetas(
    session: SessionDep,
    nombre: str = Query(..., description="Nombre o parte del nombre de la receta")
):
    resultados = session.exec(
        select(Receta).where(Receta.nombre.ilike(f"%{nombre}%"), Receta.activo == True)
    ).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron recetas con ese término")

    return resultados


@router.put("/update/{receta_id}", response_model=Receta)
async def actualizar_receta(receta_id: int, data: RecetaUpdate, session: SessionDep):
    receta = session.get(Receta, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    datos = data.model_dump(exclude_unset=True)

    if "ingredientes" in datos and isinstance(datos["ingredientes"], list):
        receta.ingredientes = datos["ingredientes"]
        del datos["ingredientes"]

    for key, value in datos.items():
        setattr(receta, key, value)

    session.add(receta)
    session.commit()
    session.refresh(receta)
    return receta


@router.delete("/kill/{receta_id}")
async def eliminar_receta(receta_id: int, session: SessionDep):
    receta = session.get(Receta, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    receta.activo = False
    session.add(receta)
    session.commit()
    return {"mensaje": f"La receta '{receta.nombre}' fue movida a la papelera."}


@router.put("/restore/{receta_id}")
async def restaurar_receta(receta_id: int, session: SessionDep):
    receta = session.get(Receta, receta_id)
    if not receta or receta.activo:
        raise HTTPException(status_code=404, detail="Receta no encontrada o ya activa")

    receta.activo = True
    session.add(receta)
    session.commit()
    return {"mensaje": f"La receta '{receta.nombre}' ha sido restaurada."}


@router.get("/trash", response_model=list[Receta])
async def listar_papelera(session: SessionDep):
    return session.exec(select(Receta).where(Receta.activo == False)).all()
