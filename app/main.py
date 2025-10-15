from fastapi import FastAPI
from app.routers import peliculas, platos, restaurantes, recetas, reportes

app = FastAPI(
    title="Disney Foods API",
    version="2.0",
    description="API para gestionar películas de Disney, los platos inspirados en ellas, restaurantes y recetas."
)

app.include_router(peliculas.router)
app.include_router(platos.router)
app.include_router(restaurantes.router)
app.include_router(recetas.router)
app.include_router(reportes.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la Disney Foods API ",
        "documentacion": "/docs",
        "mapa_endpoints": "/mapa"
    }


@app.get("/mapa")
def mapa_endpoints():
    return {
        "Películas": {
            "Crear": "/peliculas/crear",
            "Consultar todas": "/peliculas/find/all",
            "Consultar por ID": "/peliculas/find/{pelicula_id}",
            "Actualizar": "/peliculas/update/{pelicula_id}",
            "Eliminar": "/peliculas/kill/{pelicula_id}",
            "Restaurar": "/peliculas/restore/{pelicula_id}",
            "Papelera": "/peliculas/trash",
            "Buscar": "/peliculas/search?q=",
            "Filtrar": "/peliculas/filter?genero="
        },
        "Platos": {
            "Crear": "/platos/crear",
            "Consultar todos": "/platos/find/all",
            "Consultar por ID": "/platos/find/{plato_id}",
            "Actualizar": "/platos/update/{plato_id}",
            "Eliminar": "/platos/kill/{plato_id}",
            "Restaurar": "/platos/restore/{plato_id}",
            "Papelera": "/platos/trash",
            "Buscar": "/platos/search?q=",
            "Filtrar": "/platos/filter?tipo="
        },
        "Restaurantes": {
            "Crear": "/restaurantes/crear",
            "Consultar todos": "/restaurantes/find/all",
            "Consultar por ID": "/restaurantes/find/{restaurante_id}",
            "Actualizar": "/restaurantes/update/{restaurante_id}",
            "Eliminar": "/restaurantes/kill/{restaurante_id}",
            "Restaurar": "/restaurantes/restore/{restaurante_id}",
            "Papelera": "/restaurantes/trash",
            "Buscar": "/restaurantes/search?nombre_restaurante=",
            "Filtrar": "/restaurantes/filter?ubicacion="
        },
        "Recetas": {
            "Crear": "/recetas/crear",
            "Consultar todas": "/recetas/find/all",
            "Consultar por ID": "/recetas/find/{receta_id}",
            "Actualizar": "/recetas/update/{receta_id}",
            "Eliminar": "/recetas/kill/{receta_id}",
            "Restaurar": "/recetas/restore/{receta_id}",
            "Papelera": "/recetas/trash",
            "Buscar": "/recetas/search?nombre_receta=",
            "Filtrar": "/recetas/filter?dificultad="
        },
        "Reportes": {
            "Exportar CSV": "/reportes/exportar_csv"
        }
    }
