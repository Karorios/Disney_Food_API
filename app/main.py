from fastapi import FastAPI
from app.db import crear_tablas
from app.routers import peliculas, platos

app = FastAPI(
    title="Disney Foods API",
    version="1.0",
    description="API para gestionar peliculas de Disney y los platos inspirados en ellas.",
    lifespan=crear_tablas
)

app.include_router(peliculas.router)
app.include_router(platos.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la Disney Foods API",
        "documentacion": "/docs",
        "mapa_endpoints": "/mapa"
    }


@app.get("/mapa")
def mapa_endpoints():
    return {
        "Peliculas": {
            "Crear": "/peliculas/crear",
            "Consultar todas": "/peliculas/find/all",
            "Consultar por ID": "/peliculas/find/{pelicula_id}",
            "Actualizar": "/peliculas/update/{pelicula_id}",
            "Eliminar": "/peliculas/kill/{pelicula_id}"
        },
        "Platos": {
            "Crear": "/platos/crear",
            "Consultar todos": "/platos/find/all",
            "Consultar por ID": "/platos/find/{plato_id}",
            "Actualizar": "/platos/update/{plato_id}",
            "Eliminar": "/platos/kill/{plato_id}"
        }
    }
