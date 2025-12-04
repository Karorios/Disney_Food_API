import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import crear_tablas
from app.routers import peliculas, platos, restaurantes, recetas, reportes, imagenes

app = FastAPI(
    title="Disney Foods API",
    version="2.0",
    description="API para gestionar películas de Disney, los platos inspirados en ellas, restaurantes y recetas.",
)

# ✔ Crear tablas una sola vez cuando el servidor arranca
@app.on_event("startup")
def startup():
    crear_tablas()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos estáticos y templates - MONTAR ANTES de los routers
# Usar ruta absoluta para que funcione en Render
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

# Verificar que el directorio existe
if not STATIC_DIR.exists():
    raise FileNotFoundError(f"Directorio estático no encontrado: {STATIC_DIR}")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Routers - Después de montar archivos estáticos
app.include_router(peliculas.router)
app.include_router(platos.router)
app.include_router(restaurantes.router)
app.include_router(recetas.router)
app.include_router(reportes.router)
app.include_router(imagenes.router)


# Página principal
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/plato", response_class=HTMLResponse)
async def mostrar_plato(request: Request):
    data = {
        "nombre": "Ratatouille",
        "descripcion": "Un clásico plato provenzal francés...",
        "origen": "Película: Ratatouille (2007)",
        "imagen": "https://i.ytimg.com/vi/M8jQZEIdGr8/maxresdefault.jpg",
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
    }
    return templates.TemplateResponse("mapa.html", {"request": request, "endpoints": endpoints})


@app.get("/peliculas-ui", response_class=HTMLResponse)
async def peliculas_ui(request: Request):
    return templates.TemplateResponse("peliculas.html", {"request": request})


@app.get("/recetas-ui", response_class=HTMLResponse)
async def recetas_ui(request: Request):
    return templates.TemplateResponse("recetas.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Endpoint de prueba para verificar archivos estáticos
@app.get("/test-static")
async def test_static():
    import os
    BASE_DIR = Path(__file__).parent.parent
    STATIC_DIR = BASE_DIR / "app" / "static" / "js"
    api_js_path = STATIC_DIR / "api.js"
    return {
        "static_dir_exists": STATIC_DIR.exists(),
        "api_js_exists": api_js_path.exists(),
        "static_dir": str(STATIC_DIR),
        "api_js_path": str(api_js_path)
    }
