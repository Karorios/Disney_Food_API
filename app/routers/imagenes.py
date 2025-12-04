import os
import uuid

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

router = APIRouter(prefix="/imagenes", tags=["Imágenes"])


@router.post("/recetas/upload")
async def upload_receta_image(file: UploadFile = File(...)):
    """
    Sube una imagen al bucket de Supabase Storage configurado por variables de entorno
    y devuelve la URL pública.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    bucket = os.getenv("SUPABASE_BUCKET", "recetas")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail="Supabase no está configurado (SUPABASE_URL / SUPABASE_SERVICE_KEY).",
        )

    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{file_extension}"
    
    # El path en Supabase Storage es: bucket/nombre_archivo
    path = f"{bucket}/{filename}"
    
    # URL para subir el archivo (POST method)
    # Formato correcto: /storage/v1/object/{bucket}/{path}
    upload_url = f"{supabase_url}/storage/v1/object/{path}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Leer el contenido del archivo
            content = await file.read()
            
            # Subir el archivo usando POST (método correcto para Supabase Storage)
            resp = await client.post(
                upload_url,
                content=content,
                headers={
                    "Content-Type": file.content_type or "application/octet-stream",
                    "Authorization": f"Bearer {supabase_key}",
                    "x-upsert": "true",  # Permite sobrescribir si existe
                },
            )
            
            if resp.status_code >= 400:
                # Intentar parsear el error como JSON si es posible
                try:
                    error_json = resp.json()
                    error_detail = error_json.get("message", error_json.get("error", resp.text))
                except:
                    error_detail = resp.text or f"Error HTTP {resp.status_code}"
                
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al subir imagen a Supabase (HTTP {resp.status_code}): {error_detail}",
                )
                
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=500, detail="Timeout al conectar con Supabase"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error de conexión con Supabase: {str(e)}"
        )

    # URL pública del archivo subido
    public_url = f"{supabase_url}/storage/v1/object/public/{path}"
    return {"url": public_url}


