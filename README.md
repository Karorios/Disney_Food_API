# 🍽️ Disney Foods API

**Versión:** 1.0  
**Desarrollado con:** FastAPI, SQLAlchemy, SQLite  
**Autor:** Karorios

---

## Descripción

**Disney Foods API** es una aplicación desarrollada con FastAPI que permite gestionar:
- 🎬 Películas de Disney  
- 🍝 Platos inspirados en esas películas  
- 🍳 Recetas  
- 🍴 Restaurantes  

Cada modelo cuenta con operaciones CRUD completas, manejo de estado (activo/inactivo), y filtros de búsqueda personalizados.

---

## 🧩 Modelos de Datos

### 🎬 Película
| Campo | Tipo | Descripción |
|--------|------|-------------|
| `id` | int | Identificador único |
| `titulo` | str | Nombre de la película |
| `anio` | int | Año de lanzamiento |
| `genero` | str | Género de la película |
| `estado` | str | Activo o Inactivo (para eliminar sin borrar) |

Relación:  
Una película puede tener varios **platos** asociados (1:N)

---

### 🍝 Plato
| Campo | Tipo | Descripción |
|--------|------|-------------|
| `id` | int | Identificador único |
| `nombre` | str | Nombre del plato |
| `descripcion` | str | Breve detalle del plato |
| `tipo` | str | Tipo de plato (entrada, postre, bebida...) |
| `pelicula_id` | int | Relación con la película correspondiente |
| `estado` | str | Activo o Inactivo |

Relaciones:
- Un **plato** pertenece a una **película**
- Un **plato** puede tener una o varias **recetas** asociadas (1:N)

---

### 🍳 Receta
| Campo | Tipo | Descripción |
|--------|------|-------------|
| `id` | int | Identificador único |
| `nombre` | str | Nombre de la receta |
| `ingredientes` | str | Lista de ingredientes |
| `instrucciones` | str | Pasos de preparación |
| `plato_id` | int | Relación con el plato correspondiente |
| `estado` | str | Activo o Inactivo |

---

### 🍴 Restaurante
| Campo | Tipo | Descripción |
|--------|------|-------------|
| `id` | int | Identificador único |
| `nombre` | str | Nombre del restaurante |
| `ubicacion` | str | Ciudad o país |
| `especialidad` | str | Tipo de comida que ofrece |
| `estado` | str | Activo o Inactivo |

---

## ⚙️ Funcionalidades

✅ CRUD completo para cada modelo  
✅ Eliminación lógica (los datos no se borran del todo, solo se marcan como "Inactivos")  
✅ Endpoints para ver la “papelera” y restaurar registros  
✅ Filtros y búsquedas por distintos atributos  
✅ Manejo de errores y excepciones  
✅ Documentación automática en `/docs`

---

## 🧭 Mapa de Endpoints

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
