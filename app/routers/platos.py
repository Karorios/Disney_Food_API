from fastapi import APIRouter, HTTPException
from app.models import Plato, PlatoCreate, PlatoUpdate

router = APIRouter(prefix="/platos", tags=["Platos"])

platos_db = []
next_id = 1


@router.post("/crear", response_model=Plato, status_code=201)
async def crear_plato(nuevo: PlatoCreate):
    global next_id
    plato = Plato(id=next_id, **nuevo.dict())
    next_id += 1
    platos_db.append(plato)
    return plato


@router.get("/find/all", response_model=list[Plato])
async def listar_platos():
    return [p for p in platos_db if p.activo]


@router.get("/find/{plato_id}", response_model=Plato)
async def obtener_plato(plato_id: int):
    plato = next((p for p in platos_db if p.id == plato_id), None)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return plato


@router.get("/search")
async def buscar_platos(Nombre_plato: str):
    resultados = [p for p in platos_db if Nombre_plato.lower() in p.nombre.lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron platos con ese término")
    return resultados


@router.get("/filter")
async def filtrar_por_tipo(tipo: str):
    filtrados = [p for p in platos_db if p.tipo.lower() == tipo.lower()]
    return filtrados


@router.put("/update/{plato_id}", response_model=Plato)
async def actualizar_plato(plato_id: int, datos: PlatoUpdate):
    plato = next((p for p in platos_db if p.id == plato_id), None)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(plato, key, value)
    return plato


@router.delete("/kill/{plato_id}")
async def eliminar_plato(plato_id: int):
    plato = next((p for p in platos_db if p.id == plato_id), None)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    plato.activo = False
    return {"mensaje": f"El plato '{plato.nombre}' fue movido a la papelera."}


@router.get("/trash", response_model=list[Plato])
async def listar_papelera():
    return [p for p in platos_db if not p.activo]


@router.put("/restore/{plato_id}")
async def restaurar_plato(plato_id: int):
    plato = next((p for p in platos_db if p.id == plato_id and not p.activo), None)
    if not plato:
        raise HTTPException(status_code=404, detail="Plato no encontrado o ya activo")
    plato.activo = True
    return {"mensaje": f"El plato '{plato.nombre}' ha sido restaurado."}
