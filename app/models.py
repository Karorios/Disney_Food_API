from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum


class TipoComida(str, Enum):
    DULCE = "Dulce"
    SALADO = "Salado"
    BEBIDA = "Bebida"


#  MODELOS DE PELICULA
class PeliculaBase(SQLModel):
    titulo: str = Field(description="Titulo de la pelicula")
    anio: int = Field(description="Año de estreno")
    genero: str = Field(description="Genero de la pelicula")


class Pelicula(PeliculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    platos: List["Plato"] = Relationship(back_populates="pelicula")


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(SQLModel):
    titulo: Optional[str] = None
    anio: Optional[int] = None
    genero: Optional[str] = None


#  MODELOS DE PLATO
class PlatoBase(SQLModel):
    nombre: str = Field(description="Nombre del plato")
    descripcion: str = Field(description="Descripcion del plato")
    tipo_comida: TipoComida = Field(default=TipoComida.SALADO, description="Tipo de comida")


class Plato(PlatoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pelicula_id: int = Field(foreign_key="pelicula.id")
    pelicula: Pelicula = Relationship(back_populates="platos")


class PlatoCreate(PlatoBase):
    pelicula_id: int = Field(foreign_key="pelicula.id")


class PlatoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_comida: Optional[TipoComida] = None
