from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional


router = APIRouter(prefix="/restaurantes", tags=["Restaurantes"])

# ---- MODELOS ----
class RestauranteBase(BaseModel):
    nombre: str
    ubicacion: str
    tipo: str
    especialidad: Optional[str] = None


class Restaurante(RestauranteBase):
    id: int
    activo: bool = True


restaurantes_db: List[Restaurante] = []
contador = 1



# CREATE
@router.post("/crear", response_model=Restaurante, status_code=201)
def crear_restaurante(data: RestauranteBase):
    global contador
    nuevo = Restaurante(id=contador, **data.dict(), activo=True)
    restaurantes_db.append(nuevo)
    contador += 1
    return nuevo


# FIND ALL (solo activos)
@router.get("/find/all", response_model=List[Restaurante])
def listar_restaurantes():
    return [r for r in restaurantes_db if r.activo]


# FIND BY ID
@router.get("/find/{restaurante_id}", response_model=Restaurante)
def obtener_restaurante(restaurante_id: int):
    restaurante = next((r for r in restaurantes_db if r.id == restaurante_id and r.activo), None)
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado o inactivo.")
    return restaurante


# SEARCH
@router.get("/search", response_model=List[Restaurante])
def buscar_restaurantes(nombre: Optional[str] = None):
    if not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar un nombre para buscar.")
    resultados = [r for r in restaurantes_db if nombre.lower() in r.nombre.lower() and r.activo]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron restaurantes con ese nombre.")
    return resultados



@router.get("/filter", response_model=List[Restaurante])
def filtrar_restaurantes(ubicacion: Optional[str] = None, tipo: Optional[str] = None):
    resultados = [r for r in restaurantes_db if r.activo]
    if ubicacion:
        resultados = [r for r in resultados if ubicacion.lower() in r.ubicacion.lower()]
    if tipo:
        resultados = [r for r in resultados if tipo.lower() in r.tipo.lower()]
    return resultados


# TRASH
@router.get("/trash", response_model=List[Restaurante])
def listar_eliminados():
    return [r for r in restaurantes_db if not r.activo]


# UPDATE
@router.put("/update/{restaurante_id}", response_model=Restaurante)
def actualizar_restaurante(restaurante_id: int, data: RestauranteBase):
    for r in restaurantes_db:
        if r.id == restaurante_id and r.activo:
            r.nombre = data.nombre
            r.ubicacion = data.ubicacion
            r.tipo = data.tipo
            r.especialidad = data.especialidad
            return r
    raise HTTPException(status_code=404, detail="Restaurante no encontrado o inactivo.")


# DELETE
@router.delete("/kill/{restaurante_id}")
def eliminar_restaurante(restaurante_id: int):
    for r in restaurantes_db:
        if r.id == restaurante_id and r.activo:
            r.activo = False
            return {"mensaje": f"Restaurante '{r.nombre}' movido a la papelera."}
    raise HTTPException(status_code=404, detail="Restaurante no encontrado o ya eliminado.")


# RESTORE
@router.put("/restore/{restaurante_id}")
def restaurar_restaurante(restaurante_id: int):
    for r in restaurantes_db:
        if r.id == restaurante_id and not r.activo:
            r.activo = True
            return {"mensaje": f"Restaurante '{r.nombre}' restaurado exitosamente."}
    raise HTTPException(status_code=404, detail="Restaurante no encontrado o ya activo.")
