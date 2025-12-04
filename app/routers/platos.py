from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.models import Plato, PlatoCreate, PlatoUpdate
from app.db import SessionDep

router = APIRouter(prefix="/platos", tags=["Platos"])


@router.post("/crear", response_model=Plato, status_code=201)
async def crear_plato(plato_data: PlatoCreate, session: SessionDep):
    try:
        nuevo = Plato(**plato_data.model_dump())
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return nuevo
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear plato: {str(e)}")


@router.get("/find/all", response_model=list[Plato])
async def listar_platos(session: SessionDep):
    return session.exec(select(Plato).where(Plato.activo == True)).all()


@router.get("/find/{plato_id}", response_model=Plato)
async def obtener_plato(plato_id: int, session: SessionDep):
    plato = session.get(Plato, plato_id)
    if not plato or not plato.activo:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return plato


@router.get("/search", response_model=list[Plato])
async def buscar_platos(nombre: str, session: SessionDep):
    stmt = select(Plato).where(
        Plato.nombre.ilike(f"%{nombre}%"),
        Plato.activo == True
    )
    resultados = session.exec(stmt).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron platos con ese nombre")
    return resultados


@router.get("/filter", response_model=list[Plato])
async def filtrar_por_tipo(tipo: str, session: SessionDep):
    return session.exec(
        select(Plato).where(Plato.tipo.ilike(f"%{tipo}%"), Plato.activo == True)
    ).all()


@router.put("/update/{plato_id}", response_model=Plato)
async def actualizar_plato(plato_id: int, data: PlatoUpdate, session: SessionDep):
    plato = session.get(Plato, plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")

    datos = data.model_dump(exclude_unset=True)

    for key, value in datos.items():
        setattr(plato, key, value)

    session.add(plato)
    session.commit()
    session.refresh(plato)
    return plato


@router.delete("/kill/{plato_id}")
async def eliminar_plato(plato_id: int, session: SessionDep):
    plato = session.get(Plato, plato_id)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")

    plato.activo = False
    session.add(plato)
    session.commit()
    return {"mensaje": f"El plato '{plato.nombre}' fue movido a la papelera."}


@router.get("/trash", response_model=list[Plato])
async def listar_papelera(session: SessionDep):
    return session.exec(select(Plato).where(Plato.activo == False)).all()


@router.put("/restore/{plato_id}")
async def restaurar_plato(plato_id: int, session: SessionDep):
    plato = session.get(Plato, plato_id)
    if not plato or plato.activo:
        raise HTTPException(status_code=404, detail="Plato no encontrado o ya activo")

    plato.activo = True
    session.add(plato)
    session.commit()

    return {"mensaje": f"El plato '{plato.nombre}' ha sido restaurado."}
