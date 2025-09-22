"""
Utilidad ETL/ELT para la prueba técnica.

Este script obtiene registros de una API pública, los transforma a un
esquema común y los almacena en una base de datos relacional usando SQLAlchemy.

Para ejecutar este script directamente::

    python -m etl.load

La fuente de datos es configurable; por defecto usa la API de búsqueda de
Open Library porque no requiere autenticación y devuelve JSON. Puedes
cambiar ``fetch_records`` por otra API o fuente de datos local.

Variables de entorno
--------------------
``DB_URL``:
    URL de base de datos SQLAlchemy. Por defecto ``sqlite:///./data.db`` en la
    raíz del proyecto.
``OPENLIBRARY_QUERY``:
    Consulta de búsqueda para la API de Open Library. Por defecto ``colombia``.
"""
from __future__ import annotations

import os
import logging
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models_shared import Base, Item

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

def fetch_records() -> list[dict]:
    """
    Obtiene registros de una API pública externa.

    Esta implementación consulta el endpoint de búsqueda de Open Library y extrae
    información bibliográfica básica. Si eliges otro conjunto de datos, actualiza
    esta función para normalizar sus campos al esquema común definido por
    :class:`models_shared.Item`.

    Returns
    -------
    list of dict
        Lista de diccionarios que coinciden con el esquema ``Item``.
    """
    # Usar una consulta por defecto dirigida a Colombia. El usuario puede cambiarla vía env.
    query = os.getenv("OPENLIBRARY_QUERY", "colombia")
    # Limitar el número de resultados – la API soporta paginación.
    limit = 100
    url = f"https://openlibrary.org/search.json"
    params = {"q": query, "limit": limit}
    logger.info("Obteniendo registros de Open Library: %s", params)
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
    except Exception as exc:
        logger.error("Error al obtener datos: %s", exc)
        return []
    data = response.json()
    items: list[dict] = []
    for doc in data.get("docs", []):
        # Compose an identifier. The API returns keys such as "/works/OL12345W".
        work_key = doc.get("key")
        if not work_key:
            continue
        record_id = work_key.strip("/")
        title = doc.get("title") or "Untitled"
        # Extract optional fields
        date = None
        year = doc.get("first_publish_year")
        if year:
            date = str(year)
        authors = doc.get("author_name")
        if isinstance(authors, list):
            author = ", ".join(authors)
        else:
            author = None
        # Muchos docs tienen una lista 'place' que puede estar vacía.
        places = doc.get("place")
        location = None
        if isinstance(places, list) and places:
            location = ", ".join(places[:3])
        # Derivar un tipo. Para búsqueda de Open Library todos los resultados son libros.
        type_ = "book"
        summary = doc.get("subtitle") or None
        source_url = f"https://openlibrary.org{work_key}"
        items.append(
            {
                "id": record_id,
                "title": title,
                "date": date,
                "author": author,
                "location": location,
                "type": type_,
                "summary": summary,
                "source_url": source_url,
            }
        )
    logger.info("Se obtuvieron %s registros", len(items))
    return items

def run() -> None:
    """
    Ejecuta todo el pipeline de extracción-transformación-carga.

    - Obtiene registros de la API externa.
    - Crea el esquema de base de datos si no existe.
    - Inserta o actualiza cada registro en la tabla ``items``.
    """
    db_url = os.getenv("DB_URL", "sqlite:///./data.db")
    engine = create_engine(db_url, future=True)
    # Crear tablas si no existen
    Base.metadata.create_all(engine)
    records = fetch_records()
    if not records:
        logger.warning("No se obtuvieron registros; omitiendo carga.")
        return
    with Session(engine) as session:
        for record in records:
            # Usar merge para insertar/actualizar basado en clave primaria.
            session.merge(Item(**record))
        session.commit()
    logger.info("Se cargaron %s registros en la base de datos", len(records))

if __name__ == "__main__":
    run()