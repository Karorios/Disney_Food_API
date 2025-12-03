import os
import uuid

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File

router = APIRouter(prefix="/imagenes", tags=["Imágenes"])


@router.post("/recetas/upload")
async def upload_receta_image(file: UploadFile = File(...)):

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    bucket = os.getenv("SUPABASE_BUCKET", "recetas")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail="Supabase no está configurado (SUPABASE_URL / SUPABASE_SERVICE_KEY).",
        )

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = f"{bucket}/{filename}"

    upload_url = f"{supabase_url}/storage/v1/object/{path}"

    try:
        async with httpx.AsyncClient() as client:
            content = await file.read()
            resp = await client.put(
                upload_url,
                content=content,
                headers={
                    "Content-Type": file.content_type or "application/octet-stream",
                    "Authorization": f"Bearer {supabase_key}",
                },
            )
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=500,
                detail=f"Error al subir imagen a Supabase: {resp.text}",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error de conexión con Supabase: {e}"
        )

    public_url = f"{supabase_url}/storage/v1/object/public/{path}"
    return {"url": public_url}


