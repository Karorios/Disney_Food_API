from typing import Optional, List

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, Relationship


# ------------------ PELÍCULA ------------------
class PeliculaBase(SQLModel):
    titulo: str = Field(min_length=1, max_length=200)
    anio: int = Field(ge=1900, le=2100, description="Año de estreno de la película")
    genero: str = Field(min_length=1, max_length=100)


class Pelicula(PeliculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)

    # Relación 1:N con Receta
    recetas: List["Receta"] = Relationship(back_populates="pelicula")


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(SQLModel):
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=200)
    anio: Optional[int] = Field(default=None, ge=1900, le=2100)
    genero: Optional[str] = Field(default=None, min_length=1, max_length=100)
    activo: Optional[bool] = None


# ------------------ PLATO ------------------
class PlatoBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=200)
    descripcion: str = Field(min_length=1)
    tipo: str = Field(min_length=1, max_length=100)
    pelicula_id: int


class Plato(PlatoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)


class PlatoCreate(PlatoBase):
    pass


class PlatoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default=None, min_length=1)
    tipo: Optional[str] = Field(default=None, min_length=1, max_length=100)
    pelicula_id: Optional[int] = None
    activo: Optional[bool] = None


# ------------------ RESTAURANTE ------------------
class RestauranteBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=200)
    ubicacion: str = Field(min_length=1, max_length=200)
    tipo: str = Field(min_length=1, max_length=100)
    especialidad: Optional[str] = Field(default=None, max_length=200)


class Restaurante(RestauranteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)


class RestauranteCreate(RestauranteBase):
    pass


class RestauranteUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=200)
    ubicacion: Optional[str] = Field(default=None, min_length=1, max_length=200)
    tipo: Optional[str] = Field(default=None, min_length=1, max_length=100)
    especialidad: Optional[str] = Field(default=None, max_length=200)
    activo: Optional[bool] = None


# ------------------ RECETA ------------------
class RecetaBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=200)
    descripcion: str = Field(min_length=1, description="Descripción breve de la receta")
    ingredientes: List[str] = Field(
        sa_column=Column(JSON), description="Listado de ingredientes"
    )
    pasos: str = Field(min_length=1, description="Pasos detallados de preparación")
    tiempo_preparacion: int = Field(
        ge=1, le=600, description="Tiempo de preparación en minutos"
    )
    pelicula_id: int = Field(foreign_key="pelicula.id")
    imagen_url: Optional[str] = Field(
        default=None,
        description="URL pública de la imagen almacenada en Supabase u otro storage",
    )
    activo: bool = Field(default=True)


class Receta(RecetaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relación N:1 con Pelicula
    pelicula: Optional[Pelicula] = Relationship(back_populates="recetas")


class RecetaCreate(RecetaBase):
    pass


class RecetaUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default=None, min_length=1)
    ingredientes: Optional[List[str]] = None
    pasos: Optional[str] = Field(default=None, min_length=1)
    tiempo_preparacion: Optional[int] = Field(default=None, ge=1, le=600)
    pelicula_id: Optional[int] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None
