from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum


# Enumeración para tipos de comida
class TipoComida(str, Enum):
    DULCE = "Dulce"
    SALADA = "Salada"
    BEBIDA = "Bebida"


#  MODELO Pelicula
class PeliculaBase(SQLModel):
    titulo: str = Field(description="Título de la película")
    anio: int = Field(description="Año de lanzamiento")
    genero: str = Field(description="Género de la película")


class Pelicula(PeliculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True, description="Estado activo/inactivo de la película")
    platos: List["Plato"] = Relationship(back_populates="pelicula")


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(PeliculaBase):
    pass


#  MODELO PLATO
class PlatoBase(SQLModel):
    nombre: str = Field(description="Nombre del plato")
    descripcion: str = Field(description="Descripción del plato")
    tipo_comida: TipoComida = Field(default=TipoComida.SALADA, description="Tipo de comida")


class Plato(PlatoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True, description="Estado activo/inactivo del plato")
    pelicula_id: int = Field(foreign_key="pelicula.id")
    pelicula: Pelicula = Relationship(back_populates="platos")


class PlatoCreate(PlatoBase):
    pelicula_id: int = Field(foreign_key="pelicula.id")


class PlatoUpdate(PlatoBase):
    pass


# ---------- MODELO RESTAURANTE ----------
class RestauranteBase(SQLModel):
    nombre: str
    ciudad: str
    pais: str


class Restaurante(RestauranteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)
    platos: List["PlatoRestaurante"] = Relationship(back_populates="restaurante")


class RestauranteCreate(RestauranteBase):
    pass


class RestauranteUpdate(RestauranteBase):
    pass


#  RELACION PLATO - RESTAURANTE (N:N)
class PlatoRestaurante(SQLModel, table=True):
    plato_id: Optional[int] = Field(default=None, foreign_key="plato.id", primary_key=True)
    restaurante_id: Optional[int] = Field(default=None, foreign_key="restaurante.id", primary_key=True)
    restaurante: Optional[Restaurante] = Relationship(back_populates="platos")


#  MODELO RECETA
class RecetaBase(SQLModel):
    ingredientes: str
    pasos: str


class Receta(RecetaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)
    plato_id: int = Field(foreign_key="plato.id")


class RecetaCreate(RecetaBase):
    plato_id: int = Field(foreign_key="plato.id")


class RecetaUpdate(RecetaBase):
    pass
