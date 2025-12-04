# 🔧 Solución de Problemas en Render

## Problema: Los datos no se guardan en la base de datos

### Verificación 1: Variables de Entorno

Asegúrate de que todas las variables de entorno estén configuradas correctamente en Render:

1. Ve a tu servicio en Render Dashboard
2. Ve a la pestaña **Environment**
3. Verifica que estas variables estén configuradas:

```
CLEVER_USER=tu_usuario
CLEVER_PASSWORD=tu_contraseña
CLEVER_HOST=tu_host.render.com
CLEVER_PORT=5432
CLEVER_DATABASE=tu_base_datos
```

**⚠️ IMPORTANTE**: 
- El `CLEVER_HOST` en Render puede tener dos formatos:
  - Formato interno: `dpg-xxxxx-a.oregon-postgres.render.com` (para conexiones desde el mismo servicio)
  - Formato externo: `dpg-xxxxx-a.oregon-postgres.render.com` (generalmente el mismo)
  
- Si tu base de datos está en Render, usa el **host interno** que aparece en la pestaña **Info** de tu base de datos PostgreSQL.

### Verificación 2: Logs de Render

1. Ve a tu servicio en Render Dashboard
2. Ve a la pestaña **Logs**
3. Busca estos mensajes al iniciar:
   - `✅ Usando PostgreSQL: ...` - Indica que está usando PostgreSQL correctamente
   - `⚠️ Usando SQLite (fallback)` - Indica que NO está usando PostgreSQL (problema)

Si ves el mensaje de SQLite, significa que las variables de entorno no están configuradas correctamente.

### Verificación 3: Formato del Host

En Render, el host de PostgreSQL puede tener diferentes formatos. Verifica en tu base de datos PostgreSQL:

1. Ve a tu base de datos PostgreSQL en Render
2. Ve a la pestaña **Info**
3. Copia el **Internal Database URL** o el **Host** que aparece
4. Asegúrate de que `CLEVER_HOST` tenga el formato correcto

**Ejemplo de formato correcto:**
```
CLEVER_HOST=dpg-d4o99ju3jp1c73fa5pq0-a.oregon-postgres.render.com
```

**NO incluyas** `https://` o `http://` en el host.

### Verificación 4: Conexión a la Base de Datos

Si los datos no se guardan, puede ser un problema de conexión. Los logs deberían mostrar errores específicos. Busca en los logs:

- `Error al crear película: ...`
- `Error al crear receta: ...`
- Errores de conexión a PostgreSQL

### Solución: Reiniciar el Servicio

Después de cambiar las variables de entorno:

1. Ve a tu servicio en Render
2. Haz clic en **Manual Deploy** > **Clear build cache & deploy**
3. Espera a que se despliegue completamente

---

## Problema: Dashboard muestra error 404

### Solución

El endpoint de estadísticas está en `/reportes/estadisticas`, no en `/estadisticas`. Esto ya está corregido en el código, pero si aún ves el error:

1. Verifica que hayas hecho push de los últimos cambios
2. Verifica que Render haya desplegado la última versión
3. Revisa los logs para ver si hay errores al acceder a `/reportes/estadisticas`

---

## Problema: Error al subir imágenes

### Verificación

1. Verifica que `SUPABASE_URL` esté configurada correctamente
2. Verifica que `SUPABASE_SERVICE_KEY` sea la **service_role key**, no la anon key
3. Verifica que `SUPABASE_BUCKET` coincida con el nombre del bucket en Supabase
4. Verifica que el bucket en Supabase sea **público**

---

## Cómo Verificar que Todo Funciona

### 1. Verificar Conexión a Base de Datos

En los logs de Render, deberías ver:
```
✅ Usando PostgreSQL: dpg-xxxxx.render.com:5432/disney_gvkc
🔍 DATABASE_URL configurado
📦 Creando tablas en la base de datos...
✔ Tablas creadas correctamente
```

### 2. Probar Crear una Película

1. Ve a `https://tu-url.onrender.com/peliculas-ui`
2. Llena el formulario y haz clic en "Guardar"
3. Verifica que aparezca en el listado
4. Si no aparece, revisa los logs de Render para ver el error específico

### 3. Verificar Dashboard

1. Ve a `https://tu-url.onrender.com/dashboard`
2. Deberías ver los gráficos (aunque estén vacíos si no hay datos)
3. Si ves un error, revisa los logs

---

## Comandos Útiles para Debug

Si necesitas verificar la conexión manualmente, puedes agregar un endpoint temporal:

```python
@app.get("/debug/db")
def debug_db():
    from app.db import engine, DATABASE_URL
    try:
        with engine.connect() as conn:
            return {
                "status": "connected",
                "database_url": DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "hidden"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**⚠️ Recuerda eliminar este endpoint después de debuggear por seguridad.**

---

## Contacto y Soporte

Si después de seguir estos pasos aún tienes problemas:

1. Revisa los logs completos en Render
2. Verifica que todas las variables de entorno estén correctas
3. Asegúrate de que la base de datos PostgreSQL esté activa en Render
4. Verifica que el servicio web esté conectado a la base de datos correcta

