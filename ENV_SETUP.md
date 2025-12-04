# 🔧 Configuración de Variables de Entorno

Este archivo explica cómo configurar las variables de entorno necesarias para el proyecto Disney Foods API.

## 📋 Archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

### Base de Datos (Clever Cloud o PostgreSQL)

```env
# Opción 1: Variables individuales para Clever Cloud
CLEVER_USER=tu_usuario
CLEVER_PASSWORD=tu_contraseña
CLEVER_HOST=tu_host.clever-cloud.com
CLEVER_PORT=5432
CLEVER_DATABASE=tu_base_de_datos

# Opción 2: URL completa de PostgreSQL (alternativa)
# DATABASE_URL=postgresql+psycopg2://usuario:contraseña@host:puerto/base_de_datos
```

**Nota:** Si no configuras estas variables, el sistema usará SQLite local (`disney_foods.sqlite3`) como fallback para desarrollo.

### Supabase Storage (Para imágenes de recetas)

```env
# URL de tu proyecto Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co

# Service Role Key (no la anon key)
# La encuentras en: Supabase Dashboard > Settings > API > service_role key
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui

# Nombre del bucket en Supabase Storage (opcional, por defecto: "recetas")
SUPABASE_BUCKET=recetas
```

**Nota:** Si no configuras Supabase, la funcionalidad de subida de imágenes no estará disponible, pero el resto de la API funcionará normalmente.

## 🚀 Pasos para Configurar

1. **Crea el archivo `.env`** en la raíz del proyecto:
   ```bash
   touch .env
   ```

2. **Copia el contenido de ejemplo** y reemplaza con tus valores reales.

3. **Para Supabase:**
   - Ve a tu proyecto en [Supabase Dashboard](https://app.supabase.com)
   - Settings > API > Copia la `service_role` key (no la anon key)
   - Storage > Crea un bucket llamado "recetas" (o el nombre que prefieras)
   - Asegúrate de que el bucket sea público si quieres URLs públicas

4. **Para Clever Cloud:**
   - Obtén las credenciales de tu base de datos PostgreSQL
   - Configura las variables `CLEVER_*` con esos valores

## ✅ Verificación

Después de configurar, puedes verificar que las variables se cargan correctamente ejecutando:

```python
from dotenv import load_dotenv
import os

load_dotenv()
print("CLEVER_USER:", os.getenv("CLEVER_USER"))
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
```

## 🔒 Seguridad

- **NUNCA** subas el archivo `.env` a Git
- El archivo `.env` ya está en `.gitignore`
- En producción (Render, etc.), configura las variables de entorno directamente en el panel de tu plataforma

