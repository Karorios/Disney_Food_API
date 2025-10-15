from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io
import csv

from app.routers import peliculas, platos, restaurantes, recetas

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/exportar_csv")
def exportar_csv():
    output = io.StringIO()

    output.write('\ufeff')

    writer = csv.writer(output)
    writer.writerow(["Seccion", "Nombre / Titulo", "Detalle 1", "Detalle 2", "Detalle 3", "Estado"])

    # ---- Películas ----
    for p in peliculas.peliculas_db:
        writer.writerow(["Peliculas", p.titulo, p.anio, p.genero, "", "Activo" if p.activo else "Eliminado"])

    # ---- Platos ----
    for pl in platos.platos_db:
        writer.writerow(["Platos", pl.nombre, pl.descripcion, pl.tipo, "", "Activo" if pl.activo else "Eliminado"])

    # ---- Restaurantes ----
    for r in restaurantes.restaurantes_db:
        writer.writerow(["Restaurantes", r.nombre, r.ubicacion, r.tipo, r.especialidad or "",
                         "Activo" if r.activo else "Eliminado"])

    # ---- Recetas ----
    for rc in recetas.recetas_db:
        writer.writerow(["Recetas", rc.nombre, rc.descripcion, rc.dificultad, rc.tiempo_preparacion,
                         "Activo" if rc.activo else "Eliminado"])

    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=reporte_disney_foods.csv"}
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)
