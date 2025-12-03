from sqlmodel import Session

from app.db import engine, crear_tablas
from app.models import Pelicula, Receta


def run_seeds():
    crear_tablas()

    with Session(engine) as session:
        # Películas Disney base
        peliculas_data = [
            {"titulo": "Ratatouille", "anio": 2007, "genero": "Animación"},
            {"titulo": "La Bella y la Bestia", "anio": 1991, "genero": "Animación"},
            {"titulo": "La Dama y el Vagabundo", "anio": 1955, "genero": "Animación"},
            {"titulo": "Enredados", "anio": 2010, "genero": "Animación"},
        ]

        peliculas = {}
        for data in peliculas_data:
            pelicula = (
                session.query(Pelicula)
                .filter(Pelicula.titulo == data["titulo"])
                .one_or_none()
            )
            if not pelicula:
                pelicula = Pelicula(**data)
                session.add(pelicula)
                session.commit()
                session.refresh(pelicula)
            peliculas[data["titulo"]] = pelicula

        # Recetas
        recetas_data = [
            {
                "nombre": "Ratatouille",
                "descripcion": "Clásico plato provenzal de verduras al horno.",
                "ingredientes": [
                    "Berenjena",
                    "Calabacín",
                    "Pimiento rojo",
                    "Pimiento amarillo",
                    "Tomate",
                    "Aceite de oliva",
                    "Hierbas provenzales",
                ],
                "pasos": "Cortar las verduras en rodajas finas, disponer en espiral, sazonar y hornear.",
                "tiempo_preparacion": 90,
                "pelicula_titulo": "Ratatouille",
            },
            {
                "nombre": "Beignets de Tiana",
                "descripcion": "Dulces fritos esponjosos cubiertos de azúcar.",
                "ingredientes": [
                    "Harina",
                    "Levadura",
                    "Leche",
                    "Azúcar",
                    "Huevo",
                    "Aceite para freír",
                    "Azúcar glass",
                ],
                "pasos": "Preparar la masa, dejar leudar, cortar en cuadrados y freír hasta dorar.",
                "tiempo_preparacion": 60,
                "pelicula_titulo": "La Bella y la Bestia",
            },
            {
                "nombre": "Spaghetti clásico",
                "descripcion": "Pasta con salsa de tomate y albóndigas al estilo italiano.",
                "ingredientes": [
                    "Spaghetti",
                    "Carne molida",
                    "Tomate triturado",
                    "Cebolla",
                    "Ajo",
                    "Queso parmesano",
                ],
                "pasos": "Cocinar la pasta, preparar salsa con albóndigas y mezclar antes de servir.",
                "tiempo_preparacion": 45,
                "pelicula_titulo": "La Dama y el Vagabundo",
            },
            {
                "nombre": "Galletas mágicas",
                "descripcion": "Galletas dulces decoradas con formas de soles y linternas.",
                "ingredientes": [
                    "Harina",
                    "Mantequilla",
                    "Azúcar",
                    "Huevo",
                    "Vainilla",
                    "Glaseado de colores",
                ],
                "pasos": "Preparar la masa, cortar en formas mágicas, hornear y decorar.",
                "tiempo_preparacion": 40,
                "pelicula_titulo": "Enredados",
            },
        ]

        for data in recetas_data:
            pelicula = peliculas[data["pelicula_titulo"]]
            existe = (
                session.query(Receta)
                .filter(
                    Receta.nombre == data["nombre"],
                    Receta.pelicula_id == pelicula.id,
                )
                .one_or_none()
            )
            if existe:
                continue

            receta = Receta(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
                ingredientes=data["ingredientes"],
                pasos=data["pasos"],
                tiempo_preparacion=data["tiempo_preparacion"],
                pelicula_id=pelicula.id,
            )
            session.add(receta)

        session.commit()


if __name__ == "__main__":
    run_seeds()


