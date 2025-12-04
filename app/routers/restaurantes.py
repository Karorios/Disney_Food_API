from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.models import Restaurante, RestauranteCreate, RestauranteUpdate
from app.db import SessionDep

router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])


@router.post("/crear", response_model=Restaurante, status_code=201)
async def crear_restaurante(data: RestauranteCreate, session: SessionDep):
    nuevo = Restaurante(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


@router.get("/find/all", response_model=list[Restaurante])
async def listar_restaurantes(session: SessionDep):
    return session.exec(select(Restaurante).where(Restaurante.activo == True)).all()


@router.get("/find/{restaurante_id}", response_model=Restaurante)
async def obtener_restaurante(restaurante_id: int, session: SessionDep):
    restaurante = session.get(Restaurante, restaurante_id)
    if not restaurante or not restaurante.activo:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    return restaurante


@router.get("/search", response_model=list[Restaurante])
async def buscar_restaurantes(
    session: SessionDep,
    nombre: str = Query(..., description="Nombre o parte del nombre del restaurante")
):
    resultados = session.exec(
        select(Restaurante).where(Restaurante.nombre.ilike(f"%{nombre}%"), Restaurante.activo == True)
    ).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron restaurantes con ese nombre")

    return resultados


@router.get("/filter", response_model=list[Restaurante])
async def filtrar_restaurantes(
    session: SessionDep,
    ubicacion: str | None = Query(None),
    tipo: str | None = Query(None)
):
    query = select(Restaurante).where(Restaurante.activo == True)

    if ubicacion:
        query = query.where(Restaurante.ubicacion.ilike(f"%{ubicacion}%"))

    if tipo:
        query = query.where(Restaurante.tipo.ilike(f"%{tipo}%"))

    resultados = session.exec(query).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron restaurantes con esos filtros")

    return resultados


@router.put("/update/{restaurante_id}", response_model=Restaurante)
async def actualizar_restaurante(restaurante_id: int, data: RestauranteUpdate, session: SessionDep):
    restaurante = session.get(Restaurante, restaurante_id)
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")

    datos = data.model_dump(exclude_unset=True)

    for key, value in datos.items():
        setattr(restaurante, key, value)

    session.add(restaurante)
    session.commit()
    session.refresh(restaurante)
    return restaurante


@router.delete("/kill/{restaurante_id}")
async def eliminar_restaurante(restaurante_id: int, session: SessionDep):
    restaurante = session.get(Restaurante, restaurante_id)
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")

    restaurante.activo = False
    session.add(restaurante)
    session.commit()
    return {"mensaje": f"Restaurante '{restaurante.nombre}' movido a la papelera."}


@router.put("/restore/{restaurante_id}")
async def restaurar_restaurante(restaurante_id: int, session: SessionDep):
    restaurante = session.get(Restaurante, restaurante_id)
    if not restaurante or restaurante.activo:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado o ya activo")

    restaurante.activo = True
    session.add(restaurante)
    session.commit()
    return {"mensaje": f"Restaurante '{restaurante.nombre}' restaurado exitosamente."}


@router.get("/trash", response_model=list[Restaurante])
async def listar_papelera(session: SessionDep):
    return session.exec(select(Restaurante).where(Restaurante.activo == False)).all()
