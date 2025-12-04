## Disney_Food_API - Documentación del Proyecto

### Descripción y objetivo

**Disney_Food_API** es una API construida con FastAPI y SQLModel para gestionar:
- **Películas** de Disney.
- **Platos** inspirados en esas películas.
- **Recetas** asociadas a películas.
- **Restaurantes** temáticos.

El objetivo es ofrecer un backend completo con CRUDs, reportes y un **frontend ligero en Bulma** para administrar recetas y películas, además de un **dashboard** con estadísticas usando Chart.js.

---

### Modelos y relaciones

- **Pelicula**
  - `id` (int, PK)
  - `titulo` (str)
  - `anio` (int)
  - `genero` (str)
  - `activo` (bool)
  - Relación **1:N** con `Receta` (una película tiene muchas recetas).

- **Receta**
  - `id` (int, PK)
  - `nombre` (str)
  - `descripcion` (str)
  - `ingredientes` (list[str], JSON)
  - `pasos` (str)
  - `tiempo_preparacion` (int, minutos)
  - `pelicula_id` (FK a `Pelicula.id`)
  - `imagen_url` (str, opcional, URL pública de Supabase)
  - `activo` (bool)

Otras entidades:
- **Plato**: plato asociado a una película (no usado directamente en el frontend actual).
- **Restaurante**: restaurantes temáticos.

---

### CRUD explicado

- **Películas (`/peliculas`)**
  - `POST /peliculas/crear`: crea una película.
  - `GET /peliculas/find/all`: lista todas las películas activas.
  - `GET /peliculas/find/{pelicula_id}`: obtiene una película por ID.
  - `PUT /peliculas/update/{pelicula_id}`: actualiza campos de una película.
  - `DELETE /peliculas/kill/{pelicula_id}`: marcado como inactiva (papelera).
  - `GET /peliculas/trash`: lista de películas en papelera.
  - `PUT /peliculas/restore/{pelicula_id}`: restaura una película.
  - `GET /peliculas/search?nombre=`: busca por título.
  - `GET /peliculas/filter?genero=`: filtra por género.

- **Recetas (`/recetas`)**
  - `POST /recetas/crear`: crea una receta asociada a una película.
  - `GET /recetas/find/all`: lista recetas activas.
  - `GET /recetas/find/{receta_id}`: obtiene por ID.
  - `GET /recetas/search?nombre=`: busca por nombre.
  - `PUT /recetas/update/{receta_id}`: actualiza receta.
  - `DELETE /recetas/kill/{receta_id}`: mueve a papelera.
  - `PUT /recetas/restore/{receta_id}`: restaura receta.
  - `GET /recetas/trash`: lista de recetas en papelera.

- **Reportes y estadísticas (`/reportes`)**
  - `GET /reportes/exportar_csv`: genera y descarga un CSV con todas las entidades.
  - `GET /reportes/estadisticas`: agrega datos para el dashboard (número de recetas y tiempo medio por película).

- **Imágenes (`/imagenes`)**
  - `POST /imagenes/recetas/upload`: sube una imagen de receta a Supabase Storage y responde con la URL pública.

---

### Frontend: formularios y pantallas

Los templates se encuentran en `app/templates`:

- **`index.html`**: portada simple con imagen principal.
- **`peliculas.html`**:
  - Formulario para **crear/editar películas** (título, año, género).
  - Tabla de películas con acciones editar/eliminar.
  - Búsqueda por título.
- **`recetas.html`**:
  - Formulario para **crear/editar recetas**:
    - Nombre
    - Película (select)
    - Descripción
    - Ingredientes (uno por línea)
    - Pasos
    - Tiempo de preparación
    - Imagen (input `file` → subida a Supabase)
  - Tabla de recetas mostrando película y tiempo.
  - Búsqueda por nombre.
- **`dashboard.html`**:
  - Dos gráficas con Chart.js:
    - Número de recetas por película.
    - Tiempo promedio de preparación.

Todas las pantallas usan **Bulma** y un layout consistente (`base.html`, `header.html`, `footer.html`).

---

### Cómo funciona Chart.js en el dashboard

1. El template `dashboard.html` incluye el script CDN de Chart.js.
2. Un módulo JS llama a `getEstadisticas()` (definido en `static/js/api.js`).
3. El backend en `GET /reportes/estadisticas` devuelve:
   - `peliculas`: lista de títulos.
   - `recetas_por_pelicula`: lista con conteos.
   - `tiempo_promedio_preparacion`: lista con promedios (minutos).
4. Con esos arrays se crean:
   - Un gráfico de barras (recetas por película).
   - Un gráfico de línea (tiempo promedio).

---

### Endpoints detallados (resumen)

- **Películas**
  - `POST /peliculas/crear`
  - `GET /peliculas/find/all`
  - `GET /peliculas/find/{pelicula_id}`
  - `PUT /peliculas/update/{pelicula_id}`
  - `DELETE /peliculas/kill/{pelicula_id}`
  - `GET /peliculas/trash`
  - `PUT /peliculas/restore/{pelicula_id}`
  - `GET /peliculas/search?nombre=`
  - `GET /peliculas/filter?genero=`

- **Recetas**
  - `POST /recetas/crear`
  - `GET /recetas/find/all`
  - `GET /recetas/find/{receta_id}`
  - `GET /recetas/search?nombre=`
  - `PUT /recetas/update/{receta_id}`
  - `DELETE /recetas/kill/{receta_id}`
  - `PUT /recetas/restore/{receta_id}`
  - `GET /recetas/trash`

- **Platos**
  - CRUD completo en `/platos/...` (crear, find/all, find/{id}, update, kill, trash, restore, search, filter).

- **Restaurantes**
  - CRUD completo en `/restaurantes/...` con búsqueda y filtros.

- **Reportes**
  - `GET /reportes/exportar_csv`
  - `GET /reportes/estadisticas`

- **Imágenes (Supabase)**
  - `POST /imagenes/recetas/upload`

---

### Imágenes de referencia a formularios

En producción se recomiendan capturas de:
- `peliculas.html` mostrando formulario y tabla.
- `recetas.html` mostrando formulario y tabla.
- `dashboard.html` con las dos gráficas.

Estas imágenes se pueden añadir a este documento o al README como recursos visuales.

---

### Validación y manejo de errores

- **Backend (Pydantic/SQLModel)**
  - Longitud mínima y máxima para `titulo`, `genero`, `nombre`, etc.
  - `anio` restringido a 1900–2100.
  - `tiempo_preparacion` restringido a 1–600 minutos.
  - Uso de `HTTPException` 404/400/500 en casos de datos inválidos o no encontrados.

- **Frontend**
  - Formularios con atributos HTML5 (`required`, `min`, `max`, `minlength`, etc.).
  - Validación rápida en JS: si `form.checkValidity()` falla, se muestra un toast de advertencia.
  - Mensajes de éxito/error usando **toasts Bulma** implementados en `api.js`.

---

### Conclusiones

El proyecto **Disney_Food_API** queda listo como:
- Backend REST robusto con CRUDs, reportes y estadísticas.
- Frontend mínimo pero funcional con Bulma, JS moderno y fetch().
- Integración preparada para Supabase Storage para imágenes de recetas.
- Preparado para despliegue en Render u otros proveedores (CORS, estructura clara y seeds para datos iniciales).


