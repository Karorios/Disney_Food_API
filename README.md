# 🍽️ Disney Foods API

**Versión:** 2.0  
**Desarrollado con:** FastAPI, SQLAlchemy, PostgreSQL, Supabase  
**Autor:** Karorios

---

## Descripción

**Disney Foods API** es una aplicación desarrollada con FastAPI que permite gestionar:
- 🎬 Películas de Disney  
- 🍝 Platos inspirados en esas películas  
- 🍳 Recetas  
- 🍴 Restaurantes  

Cada modelo cuenta con operaciones CRUD completas, manejo de estado (activo/inactivo), y filtros de búsqueda personalizados.

## 🚀 Despliegue

Este proyecto está configurado para desplegarse en **Render**. Para instrucciones detalladas, consulta el archivo [RENDER_DEPLOY.md](RENDER_DEPLOY.md).

### Configuración Rápida

1. **Base de Datos**: PostgreSQL en Render
2. **Storage de Imágenes**: Supabase Storage
3. **Variables de Entorno**: Configurar en el panel de Render

Ver [RENDER_DEPLOY.md](RENDER_DEPLOY.md) para la guía completa de despliegue.

---


## ⚙️ Funcionalidades

CRUD completo para cada modelo  
Eliminación lógica (los datos no se borran del todo, solo se marcan como "Inactivos")  
Endpoints para ver la “papelera” y restaurar registros  
Filtros y búsquedas por distintos atributos  
Manejo de errores y excepciones  
Documentación automática en `/docs`

---

## Mapa de Endpoints

| Categoría | Acción | Endpoint | Método |
|------------|--------|-----------|--------|
| 🎬 Películas | Crear | `/peliculas/crear` | POST |
|  | Listar todas | `/peliculas/find/all` | GET |
|  | Consultar por ID | `/peliculas/find/{id}` | GET |
|  | Actualizar | `/peliculas/update/{id}` | PUT |
|  | Eliminar (papelera) | `/peliculas/kill/{id}` | DELETE |
|  | Listar eliminadas | `/peliculas/papelera` | GET |
|  | Restaurar eliminada | `/peliculas/restore/{id}` | PATCH |
|  | Filtrar por género | `/peliculas/filter/?genero=` | GET |
|  | Buscar por palabra | `/peliculas/search/?q=` | GET |
| 🍝 Platos | Crear | `/platos/crear` | POST |
|  | Listar todos | `/platos/find/all` | GET |
|  | Consultar por ID | `/platos/find/{id}` | GET |
|  | Actualizar | `/platos/update/{id}` | PUT |
|  | Eliminar (papelera) | `/platos/kill/{id}` | DELETE |
|  | Listar eliminados | `/platos/papelera` | GET |
|  | Restaurar eliminado | `/platos/restore/{id}` | PATCH |
|  | Filtrar por tipo | `/platos/filter/?tipo=` | GET |
|  | Buscar por palabra | `/platos/search/?q=` | GET |
| 🍳 Recetas | CRUD y restauración | `/recetas/...` |  |
| 🍴 Restaurantes | CRUD y restauración | `/restaurantes/...` |  |

---

## 💾 Ejemplos de Uso

**Crear película**
```bash
POST /peliculas/crear
{
  "titulo": "Encanto",
  "anio": 2021,
  "genero": "Animación"
}
