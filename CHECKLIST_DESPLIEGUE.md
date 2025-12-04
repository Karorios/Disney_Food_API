# ✅ Checklist de Despliegue en Render

Usa este checklist para asegurarte de que todo esté configurado correctamente.

## 📋 Antes de Desplegar

### Supabase
- [ ] Tienes un proyecto creado en Supabase
- [ ] Has creado un bucket llamado `recetas` (o el nombre que prefieras)
- [ ] El bucket está marcado como **Público** (Public bucket)
- [ ] Tienes tu **Project URL** de Supabase (ejemplo: `https://xxxxx.supabase.co`)
- [ ] Tienes tu **service_role key** (NO la anon key)
  - Ubicación: Supabase Dashboard > Settings > API > service_role key

### Base de Datos PostgreSQL en Render
- [ ] Tienes una base de datos PostgreSQL creada en Render
- [ ] Tienes las siguientes credenciales:
  - [ ] Host (ejemplo: `dpg-xxxxx.render.com`)
  - [ ] Port (generalmente `5432`)
  - [ ] Database name
  - [ ] User
  - [ ] Password

### Repositorio Git
- [ ] Tu código está en GitHub, GitLab o Bitbucket
- [ ] Has hecho commit de todos los cambios
- [ ] Has hecho push al repositorio

---

## 🚀 Durante el Despliegue en Render

### Configuración del Servicio
- [ ] Has conectado tu repositorio a Render
- [ ] Has seleccionado el repositorio correcto
- [ ] Render detectó automáticamente el archivo `render.yaml` (o configuraste manualmente)

### Variables de Entorno en Render
Configura estas variables en Render > Environment:

#### Base de Datos
- [ ] `CLEVER_USER` = tu usuario de PostgreSQL
- [ ] `CLEVER_PASSWORD` = tu contraseña de PostgreSQL
- [ ] `CLEVER_HOST` = tu host de PostgreSQL (ejemplo: `dpg-xxxxx.render.com`)
- [ ] `CLEVER_PORT` = `5432` (o el puerto correcto)
- [ ] `CLEVER_DATABASE` = nombre de tu base de datos

#### Supabase
- [ ] `SUPABASE_URL` = tu Project URL (ejemplo: `https://xxxxx.supabase.co`)
- [ ] `SUPABASE_SERVICE_KEY` = tu service_role key
- [ ] `SUPABASE_BUCKET` = `recetas` (o el nombre de tu bucket)

---

## ✅ Después del Despliegue

### Verificación
- [ ] El servicio se desplegó sin errores
- [ ] Puedes acceder a `https://tu-url.onrender.com/docs`
- [ ] La documentación de la API se muestra correctamente
- [ ] Puedes hacer peticiones a los endpoints (GET, POST, etc.)

### Prueba de Funcionalidades
- [ ] La base de datos funciona (puedes crear/leer datos)
- [ ] Puedes subir una imagen usando `/imagenes/recetas/upload`
- [ ] La imagen se sube correctamente a Supabase
- [ ] Recibes una URL pública de la imagen

---

## 🔧 Si Algo No Funciona

### Error: "Supabase no está configurado"
- [ ] Verifica que `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` estén configuradas
- [ ] Asegúrate de que no tengan espacios extra
- [ ] Reinicia el servicio después de agregar las variables

### Error: "Error al subir imagen a Supabase"
- [ ] Verifica que el bucket existe en Supabase
- [ ] Verifica que el bucket sea **público**
- [ ] Verifica que estás usando la `service_role` key (no la anon key)
- [ ] Verifica que la URL de Supabase sea correcta

### Error de conexión a la base de datos
- [ ] Verifica todas las variables `CLEVER_*`
- [ ] Verifica que la base de datos esté activa en Render
- [ ] Verifica que el host, puerto, usuario y contraseña sean correctos

### La aplicación no inicia
- [ ] Revisa los **Logs** en Render para ver el error específico
- [ ] Verifica que `requirements.txt` tenga todas las dependencias
- [ ] Verifica que el comando de inicio sea: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 📞 Recursos

- [Guía Completa de Despliegue](RENDER_DEPLOY.md)
- [Configuración de Variables de Entorno](ENV_SETUP.md)
- [Documentación del Proyecto](documentacion_proyecto.md)

---

**¡Una vez que completes todos los pasos, tu API debería estar funcionando al 100%! 🎉**

