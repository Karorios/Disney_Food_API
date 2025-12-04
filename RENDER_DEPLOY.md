# 🚀 Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu API Disney Foods en Render y configurar Supabase para que las imágenes funcionen correctamente.

## 📋 Prerrequisitos

1. Cuenta en [Render](https://render.com)
2. Base de datos PostgreSQL en Render (ya la tienes configurada)
3. Proyecto en Supabase para almacenar imágenes
4. Repositorio Git (GitHub, GitLab, o Bitbucket)

---

## 🔧 Paso 1: Configurar Supabase

### 1.1 Crear un proyecto en Supabase (si no lo tienes)

1. Ve a [Supabase Dashboard](https://app.supabase.com)
2. Crea un nuevo proyecto o usa uno existente
3. Espera a que el proyecto esté completamente inicializado

### 1.2 Crear el bucket de Storage

1. En tu proyecto de Supabase, ve a **Storage** en el menú lateral
2. Haz clic en **New bucket**
3. Nombre del bucket: `recetas` (o el que prefieras)
4. **IMPORTANTE**: Marca la casilla **Public bucket** para que las imágenes sean accesibles públicamente
5. Haz clic en **Create bucket**

### 1.3 Obtener las credenciales de Supabase

1. Ve a **Settings** > **API** en tu proyecto de Supabase
2. Encuentra la sección **Project URL** y copia la URL (ejemplo: `https://xxxxx.supabase.co`)
3. En la sección **Project API keys**, busca la clave **`service_role`** (⚠️ NO uses la `anon` key)
4. Copia la `service_role` key

**⚠️ IMPORTANTE**: La `service_role` key tiene permisos completos. NUNCA la expongas en el frontend o código público.

---

## 🚀 Paso 2: Desplegar en Render

### 2.1 Conectar el repositorio

1. Inicia sesión en [Render Dashboard](https://dashboard.render.com)
2. Haz clic en **New +** > **Web Service**
3. Conecta tu repositorio Git (GitHub, GitLab, o Bitbucket)
4. Selecciona el repositorio `Disney_Food_API`

### 2.2 Configurar el servicio

Render debería detectar automáticamente el archivo `render.yaml`, pero puedes configurarlo manualmente:

- **Name**: `disney-foods-api` (o el nombre que prefieras)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free (o el plan que prefieras)

### 2.3 Configurar Variables de Entorno

En la sección **Environment Variables** de Render, agrega las siguientes variables:

#### Variables de Base de Datos (PostgreSQL en Render)

Obtén estas credenciales de tu base de datos PostgreSQL en Render:

```
CLEVER_USER=tu_usuario_postgres
CLEVER_PASSWORD=tu_contraseña_postgres
CLEVER_HOST=tu_host_postgres.render.com
CLEVER_PORT=5432
CLEVER_DATABASE=tu_nombre_base_datos
```

**Cómo obtenerlas:**
1. Ve a tu base de datos PostgreSQL en Render
2. En la pestaña **Info**, encontrarás:
   - **Host**: `CLEVER_HOST`
   - **Port**: `CLEVER_PORT` (generalmente 5432)
   - **Database**: `CLEVER_DATABASE`
   - **User**: `CLEVER_USER`
   - **Password**: `CLEVER_PASSWORD` (haz clic en "Show" para verla)

#### Variables de Supabase

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui
SUPABASE_BUCKET=recetas
```

**Reemplaza:**
- `https://tu-proyecto.supabase.co` con tu Project URL de Supabase
- `tu_service_role_key_aqui` con tu service_role key de Supabase
- `recetas` con el nombre de tu bucket (si usaste otro nombre)

### 2.4 Desplegar

1. Haz clic en **Create Web Service**
2. Render comenzará a construir y desplegar tu aplicación
3. Espera a que el despliegue termine (puede tomar 2-5 minutos)

---

## ✅ Paso 3: Verificar el Despliegue

### 3.1 Verificar que la API funciona

1. Una vez desplegado, Render te dará una URL como: `https://disney-foods-api.onrender.com`
2. Visita: `https://tu-url.onrender.com/docs` para ver la documentación de la API
3. Prueba algunos endpoints para verificar que todo funciona

### 3.2 Verificar que Supabase está configurado

1. Intenta subir una imagen usando el endpoint `/imagenes/recetas/upload`
2. Si todo está bien configurado, deberías recibir una URL pública de la imagen
3. Si ves un error sobre Supabase no configurado, verifica que las variables de entorno estén correctamente configuradas en Render

---

## 🔍 Solución de Problemas

### Error: "Supabase no está configurado"

**Causa**: Las variables de entorno de Supabase no están configuradas o tienen valores incorrectos.

**Solución**:
1. Ve a tu servicio en Render > **Environment**
2. Verifica que `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` estén configuradas
3. Asegúrate de que no tengan espacios extra al inicio o final
4. Reinicia el servicio después de agregar/modificar variables

### Error: "Error al subir imagen a Supabase"

**Causa**: El bucket no existe, no es público, o la service_role key es incorrecta.

**Solución**:
1. Verifica que el bucket `recetas` existe en Supabase Storage
2. Asegúrate de que el bucket sea **público**
3. Verifica que estás usando la `service_role` key, no la `anon` key
4. Verifica que la URL de Supabase sea correcta (debe terminar en `.supabase.co`)

### Error de conexión a la base de datos

**Causa**: Las credenciales de PostgreSQL no están correctas.

**Solución**:
1. Verifica todas las variables `CLEVER_*` en Render
2. Asegúrate de que la base de datos esté activa en Render
3. Verifica que el host, puerto, usuario y contraseña sean correctos

### La aplicación no inicia

**Causa**: Error en el código o dependencias faltantes.

**Solución**:
1. Ve a **Logs** en Render para ver el error específico
2. Verifica que `requirements.txt` tenga todas las dependencias
3. Verifica que el comando de inicio sea correcto: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 📝 Notas Importantes

1. **Variables de Entorno**: Nunca subas el archivo `.env` a Git. Render usa las variables configuradas en su panel.

2. **Service Role Key**: Esta clave tiene permisos completos. Solo úsala en el backend, nunca en el frontend.

3. **Bucket Público**: Si el bucket no es público, las imágenes no serán accesibles públicamente. Asegúrate de marcarlo como público en Supabase.

4. **Reinicio del Servicio**: Después de cambiar variables de entorno, Render reiniciará automáticamente el servicio.

5. **Plan Free**: En el plan gratuito de Render, el servicio se "duerme" después de 15 minutos de inactividad. La primera petición después de dormir puede tardar ~30 segundos.

---

## 🎉 ¡Listo!

Si seguiste todos los pasos, tu API debería estar funcionando al 100% en Render con:
- ✅ Base de datos PostgreSQL conectada
- ✅ Supabase configurado para subir imágenes
- ✅ Todos los endpoints funcionando

Si tienes algún problema, revisa los logs en Render o verifica la configuración de las variables de entorno.

