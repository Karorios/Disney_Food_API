from pydantic import BaseModel
from typing import Optional, List


class PeliculaBase(BaseModel):
    titulo: str
    anio: int
    genero: str


class Pelicula(PeliculaBase):
    id: int
    activo: bool = True


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaUpdate(BaseModel):
    titulo: Optional[str] = None
    anio: Optional[int] = None
    genero: Optional[str] = None
    activo: Optional[bool] = None


class PlatoBase(BaseModel):
    nombre: str
    descripcion: str
    tipo: str
    pelicula_id: int


class Plato(PlatoBase):
    id: int
    activo: bool = True


class PlatoCreate(PlatoBase):
    pass


class PlatoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    pelicula_id: Optional[int] = None
    activo: Optional[bool] = None
