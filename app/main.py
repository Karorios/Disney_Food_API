from fastapi import FastAPI
from app.db import crear_tablas
from app.routers import peliculas, platos, restaurantes, recetas

app = FastAPI(
    title="Disney Foods API",
    version="2.0",
    description="API para gestionar películas de Disney, platos inspirados, restaurantes y recetas.",
    lifespan=crear_tablas
)

app.include_router(peliculas.router)
app.include_router(platos.router)
app.include_router(restaurantes.router)
app.include_router(recetas.router)

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
            "Consultar eliminadas": "/peliculas/inactivas",
            "Actualizar": "/peliculas/update/{pelicula_id}",
            "Eliminar (a papelera)": "/peliculas/kill/{pelicula_id}",
            "Restaurar": "/peliculas/restore/{pelicula_id}"
        },
        "Platos": {
            "Crear": "/platos/crear",
            "Consultar todos": "/platos/find/all",
            "Consultar por ID": "/platos/find/{plato_id}",
            "Consultar eliminados": "/platos/inactivos",
            "Actualizar": "/platos/update/{plato_id}",
            "Eliminar (a papelera)": "/platos/kill/{plato_id}",
            "Restaurar": "/platos/restore/{plato_id}"
        },
        "Restaurantes": {
            "Crear": "/restaurantes/crear",
            "Consultar todos": "/restaurantes/find/all",
            "Consultar por ID": "/restaurantes/find/{restaurante_id}",
            "Consultar eliminados": "/restaurantes/inactivos",
            "Actualizar": "/restaurantes/update/{restaurante_id}",
            "Eliminar (a papelera)": "/restaurantes/kill/{restaurante_id}",
            "Restaurar": "/restaurantes/restore/{restaurante_id}"
        },
        "Recetas": {
            "Crear": "/recetas/crear",
            "Consultar todas": "/recetas/find/all",
            "Consultar por ID": "/recetas/find/{receta_id}",
            "Consultar eliminadas": "/recetas/inactivos",
            "Actualizar": "/recetas/update/{receta_id}",
            "Eliminar (a papelera)": "/recetas/kill/{receta_id}",
            "Restaurar": "/recetas/restore/{receta_id}"
        }
    }
