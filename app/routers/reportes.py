import csv
from fastapi import APIRouter
from fastapi.responses import FileResponse
from sqlmodel import select
from app.db import SessionDep
from app.models import Pelicula, Plato, Restaurante, Receta

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/exportar_csv")
async def exportar_csv(session: SessionDep):
    """Genera un reporte CSV de todas las entidades activas."""
    with open("reporte_disney_foods.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Entidad", "Nombre/Título", "Campo adicional", "Activo"])

        # Películas
        for p in session.exec(select(Pelicula)).all():
            writer.writerow(["Pelicula", p.titulo, p.genero, p.activo])

        # Platos
        for pl in session.exec(select(Plato)).all():
            writer.writerow(["Plato", pl.nombre, pl.tipo, pl.activo])

        # Restaurantes
        for r in session.exec(select(Restaurante)).all():
            writer.writerow(["Restaurante", r.nombre, r.tipo, r.activo])

        # Recetas
        for rc in session.exec(select(Receta)).all():
            writer.writerow(["Receta", rc.nombre, rc.ingredientes, rc.activo])

    return FileResponse("reporte_disney_foods.csv", filename="reporte_disney_foods.csv")
