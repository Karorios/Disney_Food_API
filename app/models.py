from typing import Optional, List, Union
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlmodel import JSON
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON

class PeliculaBase(SQLModel):
    titulo: str
    anio: int
    genero: str


class Pelicula(PeliculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(SQLModel):
    titulo: Optional[str] = None
    anio: Optional[int] = None
    genero: Optional[str] = None
    activo: Optional[bool] = None


# ------------------ PLATO ------------------
class PlatoBase(SQLModel):
    nombre: str
    descripcion: str
    tipo: str
    pelicula_id: int


class Plato(PlatoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)


class PlatoCreate(PlatoBase):
    pass


class PlatoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    pelicula_id: Optional[int] = None
    activo: Optional[bool] = None


# ------------------ RESTAURANTE ------------------
class RestauranteBase(SQLModel):
    nombre: str
    ubicacion: str
    tipo: str
    especialidad: Optional[str] = None


class Restaurante(RestauranteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)


class RestauranteCreate(RestauranteBase):
    pass


class RestauranteUpdate(SQLModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    tipo: Optional[str] = None
    especialidad: Optional[str] = None
    activo: Optional[bool] = None


from typing import Optional
from sqlmodel import SQLModel, Field


# ------------------ RECETA ------------------
class RecetaBase(SQLModel):
    nombre: str
    ingredientes: list[str] = Field(sa_column=Column(JSON))
    instrucciones: str
    plato_id: int | None = Field(default=None, foreign_key="plato.id")
    activo: bool = True

class Receta(RecetaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class RecetaCreate(RecetaBase):
    pass

class RecetaUpdate(SQLModel):
    nombre: str | None = None
    ingredientes: list[str] | None = None
    instrucciones: str | None = None
    plato_id: int | None = None
