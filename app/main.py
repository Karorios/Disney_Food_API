from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import crear_tablas
from app.routers import peliculas, platos, restaurantes, recetas, reportes

app = FastAPI(
    title="Disney Foods API",
    version="2.0",
    description="API para gestionar peliculas de Disney, los platos inspirados en ellas, restaurantes y recetas."
)

crear_tablas()

app.include_router(peliculas.router)
app.include_router(platos.router)
app.include_router(restaurantes.router)
app.include_router(recetas.router)
app.include_router(reportes.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Página principal
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Página para mostrar un plato
@app.get("/plato", response_class=HTMLResponse)
async def mostrar_plato(request: Request):
    data = {
        "nombre": "Ratatouille",
        "descripcion": "Un clásico plato provenzal francés con berenjena, calabacín, pimientos y tomate, hecho famoso por la película de Disney-Pixar.",
        "origen": "Película: Ratatouille (2007)",
        "imagen": "https://i.ytimg.com/vi/M8jQZEIdGr8/maxresdefault.jpg"
    }
    return templates.TemplateResponse("plato.html", {"request": request, "plato": data})

@app.get("/mapa", response_class=HTMLResponse)
async def mapa_endpoints(request: Request):
    endpoints = {
        "Películas": [
            {"accion": "Crear", "url": "/peliculas/crear"},
            {"accion": "Consultar todas", "url": "/peliculas/find/all"},
            {"accion": "Consultar por ID", "url": "/peliculas/find/{pelicula_id}"},
            {"accion": "Actualizar", "url": "/peliculas/update/{pelicula_id}"},
            {"accion": "Eliminar", "url": "/peliculas/kill/{pelicula_id}"},
            {"accion": "Restaurar", "url": "/peliculas/restore/{pelicula_id}"},
            {"accion": "Papelera", "url": "/peliculas/trash"},
            {"accion": "Buscar", "url": "/peliculas/search?q="},
            {"accion": "Filtrar", "url": "/peliculas/filter?genero="}
        ],
        "Platos": [
            {"accion": "Crear", "url": "/platos/crear"},
            {"accion": "Consultar todos", "url": "/platos/find/all"},
            {"accion": "Consultar por ID", "url": "/platos/find/{plato_id}"},
            {"accion": "Actualizar", "url": "/platos/update/{plato_id}"},
            {"accion": "Eliminar", "url": "/platos/kill/{plato_id}"},
            {"accion": "Restaurar", "url": "/platos/restore/{plato_id}"},
            {"accion": "Papelera", "url": "/platos/trash"},
            {"accion": "Buscar", "url": "/platos/search?q="},
            {"accion": "Filtrar", "url": "/platos/filter?tipo="}
        ],
        "Restaurantes": [
            {"accion": "Crear", "url": "/restaurantes/crear"},
            {"accion": "Consultar todos", "url": "/restaurantes/find/all"},
            {"accion": "Consultar por ID", "url": "/restaurantes/find/{restaurante_id}"},
            {"accion": "Actualizar", "url": "/restaurantes/update/{restaurante_id}"},
            {"accion": "Eliminar", "url": "/restaurantes/kill/{restaurante_id}"},
            {"accion": "Restaurar", "url": "/restaurantes/restore/{restaurante_id}"},
            {"accion": "Papelera", "url": "/restaurantes/trash"},
            {"accion": "Buscar", "url": "/restaurantes/search?nombre_restaurante="},
            {"accion": "Filtrar", "url": "/restaurantes/filter?ubicacion="}
        ],
        "Recetas": [
            {"accion": "Crear", "url": "/recetas/crear"},
            {"accion": "Consultar todas", "url": "/recetas/find/all"},
            {"accion": "Consultar por ID", "url": "/recetas/find/{receta_id}"},
            {"accion": "Actualizar", "url": "/recetas/update/{receta_id}"},
            {"accion": "Eliminar", "url": "/recetas/kill/{receta_id}"},
            {"accion": "Restaurar", "url": "/recetas/restore/{receta_id}"},
            {"accion": "Papelera", "url": "/recetas/trash"},
            {"accion": "Buscar", "url": "/recetas/search?nombre_receta="},
            {"accion": "Filtrar", "url": "/recetas/filter?dificultad="}
        ]
    }
    return templates.TemplateResponse("mapa.html", {"request": request, "endpoints": endpoints})
