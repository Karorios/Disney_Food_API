from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/recetas", tags=["Recetas"])

# ---- MODELOS ----
class RecetaBase(BaseModel):
    nombre: str
    ingredientes: List[str]
    instrucciones: str
    plato_id: Optional[int] = None

class Receta(RecetaBase):
    id: int
    activo: bool = True

# ---- BASE EN MEMORIA ----
recetas_db: List[Receta] = []
contador = 1


# ---- ENDPOINTS ----
@router.post("/crear", response_model=Receta)
def crear_receta(data: RecetaBase):
    global contador
    nueva = Receta(id=contador, **data.dict(), activo=True)
    recetas_db.append(nueva)
    contador += 1
    return nueva





@router.get("/find/all", response_model=List[Receta])
def listar_recetas():
    return [r for r in recetas_db if r.activo]

@router.get("/search", response_model=List[Receta])
def buscar_recetas(nombre_receta: str):
    resultados = [r for r in recetas_db if nombre_receta.lower() in r.nombre.lower() and r.activo]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron recetas con ese nombre.")
    return resultados

@router.get("/find/{receta_id}", response_model=Receta)
def obtener_receta(receta_id: int):
    receta = next((r for r in recetas_db if r.id == receta_id and r.activo), None)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta


@router.put("/update/{receta_id}", response_model=Receta)
def actualizar_receta(receta_id: int, data: RecetaBase):
    for r in recetas_db:
        if r.id == receta_id and r.activo:
            r.nombre = data.nombre
            r.ingredientes = data.ingredientes
            r.instrucciones = data.instrucciones
            r.plato_id = data.plato_id
            return r
    raise HTTPException(status_code=404, detail="Receta no encontrada o inactiva")


@router.delete("/kill/{receta_id}")
def eliminar_receta(receta_id: int):
    for r in recetas_db:
        if r.id == receta_id and r.activo:
            r.activo = False
            return {"mensaje": f"Receta '{r.nombre}' movida a la papelera."}
    raise HTTPException(status_code=404, detail="Receta no encontrada o ya eliminada")


@router.get("/trash", response_model=List[Receta])
def listar_eliminadas():
    return [r for r in recetas_db if not r.activo]


@router.put("/restore/{receta_id}")
def restaurar_receta(receta_id: int):
    for r in recetas_db:
        if r.id == receta_id and not r.activo:
            r.activo = True
            return {"mensaje": f"Receta '{r.nombre}' restaurada exitosamente."}
    raise HTTPException(status_code=404, detail="Receta no encontrada o ya activa")


