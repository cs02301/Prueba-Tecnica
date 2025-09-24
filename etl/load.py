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
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models_shared import Base, Item

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

def _fallback_records() -> list[dict]:
    """
    Conjunto de datos de respaldo para casos en que la API externa no esté disponible.
    Devuelve unos pocos ítems representativos con los campos esperados.
    """
    return [
        {
            "id": "sample/it",
            "title": "It",
            "date": "1986",
            "author": "Stephen King",
            "location": "Estados Unidos",
            "type": "book",
            "summary": "Novela de terror de un ente malévolo en Derry.",
            "source_url": "https://openlibrary.org/works/OL45804W",
            "genre": "horror, terror, fiction",
        },
        {
            "id": "sample/amor-colera",
            "title": "El amor en los tiempos del cólera",
            "date": "1985",
            "author": "Gabriel García Márquez",
            "location": "Colombia",
            "type": "book",
            "summary": "Historia de amor entre Florentino y Fermina.",
            "source_url": "https://openlibrary.org/works/OL15312747W",
            "genre": "romance, realismo mágico, romance",
        },
        {
            "id": "sample/cronica",
            "title": "Crónica de una muerte anunciada",
            "date": "1980",
            "author": "Gabriel García Márquez",
            "location": "Caribe colombiano",
            "type": "book",
            "summary": "Relato sobre un crimen anunciado por todo el pueblo.",
            "source_url": "https://openlibrary.org/works/OL82563W",
            "genre": "crime, crimen, realismo mágico",
        },
        {
            "id": "sample/picasso",
            "title": "Picasso",
            "date": "1926",
            "author": "Pablo Picasso, Jean-Louis Andral, Pierre Daix",
            "location": "Francia",
            "type": "book",
            "summary": "Obra sobre Pablo Picasso.",
            "source_url": "https://openlibrary.org/works/OL12345W",
            "genre": "art, arte, biography, biografía",
        },
        {
            "id": "sample/das-kapital",
            "title": "Das Kapital",
            "date": "1867",
            "author": "Karl Marx",
            "location": "Alemania",
            "type": "book",
            "summary": "Análisis crítico del capitalismo.",
            "source_url": "https://openlibrary.org/works/OL20638W",
            "genre": "economics, economía, philosophy, filosofía, physics",
        },
    ]

def _get_with_retries(url: str, params: dict, retries: int = 3, backoff: float = 2.0) -> requests.Response:
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return requests.get(url, params=params, timeout=30)
        except Exception as exc:
            last_exc = exc
            logger.warning("Intento %s/%s fallido: %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(backoff ** attempt)
    if last_exc:
        raise last_exc

def ensure_schema(engine) -> None:
    """
    Asegura que el esquema tenga las columnas esperadas.

    En SQLite, ``create_all`` no agrega nuevas columnas, así que
    hacemos una verificación ligera y agregamos ``genre`` si falta.
    """
    try:
        with engine.begin() as conn:
            res = conn.exec_driver_sql("PRAGMA table_info(items)")
            cols = {row[1] for row in res}
            if 'genre' not in cols:
                logging.info("Agregando columna 'genre' a la tabla items...")
                conn.exec_driver_sql("ALTER TABLE items ADD COLUMN genre VARCHAR")
                logging.info("Columna 'genre' agregada")
    except Exception as exc:
        logging.warning("No se pudo verificar/alterar el esquema: %s", exc)

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
        response = _get_with_retries(url, params)
        response.raise_for_status()
    except Exception as exc:
        logger.error("Error al obtener datos: %s", exc)
        logger.warning("Usando datos locales de respaldo para continuar.")
        return _fallback_records()
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
        # Subjects can serve as genres/tags; try multiple fields from Open Library
        subjects = (
            doc.get("subject")
            or doc.get("subject_facet")
            or doc.get("subject_key")
            or doc.get("subject_place")
            or doc.get("subject_person")
            or doc.get("subject_time")
        )
        genre = None
        if isinstance(subjects, list) and subjects:
            # keep a few top subjects
            genre = ", ".join(subjects[:5])

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
                "genre": genre,
            }
        )
    logger.info("Se obtuvieron %s registros", len(items))
    return items

def enrich_missing_genres(items: list[dict], max_enrich: int = 20) -> None:
    """
    Enriquecimiento ligero: para ítems sin género, consulta el endpoint
    de la obra en Open Library (/{id}.json) y toma sus 'subjects'.

    Limita a 'max_enrich' solicitudes para mantener la ejecución rápida.
    """
    enriched = 0
    for rec in items:
        if enriched >= max_enrich:
            break
        if rec.get('genre'):
            continue
        rec_id = rec.get('id')
        if not rec_id:
            continue
        url = f"https://openlibrary.org/{rec_id}.json"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                subs = data.get('subjects')
                if isinstance(subs, list) and subs:
                    rec['genre'] = ", ".join([str(s) for s in subs[:5]])
                    enriched += 1
        except Exception as exc:
            logger.debug("No se pudo enriquecer %s: %s", rec_id, exc)

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
    # Asegurar columnas nuevas (p.ej., genre)
    ensure_schema(engine)
    records = fetch_records()
    # Enriquecer géneros faltantes con un número limitado de requests
    if records:
        enrich_missing_genres(records, max_enrich=25)
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