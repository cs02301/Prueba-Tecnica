"""
Aplicación FastAPI que sirve el conjunto de datos de la prueba técnica.

La API expone endpoints para listar, buscar y recuperar elementos individuales,
así como un endpoint administrativo protegido para refrescar la base de datos
ejecutando nuevamente el proceso ETL.
"""
from __future__ import annotations

import os
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, Header, Query, status
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session
from typing import Generator

from models_shared import Base, Item
from etl.load import run as etl_run  # reuse the ETL to refresh data

from pydantic import BaseModel

class ItemOut(BaseModel):
    id: str
    title: str
    date: Optional[str] = None
    author: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    summary: Optional[str] = None
    source_url: Optional[str] = None
    genre: Optional[str] = None

    class Config:
        from_attributes = True

class GenreOut(BaseModel):
    name: str
    count: int

DB_URL = os.getenv("DB_URL", "sqlite:///./data.db")
API_KEY = os.getenv("API_KEY", "dev-key")

# Crear el engine una vez al importar el módulo. Con SQLite esto creará
# el archivo de base de datos en el directorio de trabajo si no existe.
engine = create_engine(DB_URL, future=True)

def get_session() -> Generator[Session, None, None]:
    """
    Dependencia que proporciona una sesión de base de datos para una petición.
    La sesión se cierra después de enviar la respuesta.
    """
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="API de Ítems Públicos",
    description=(
        "Una API REST simple para acceder a registros públicos normalizados. "
        "Puedes listar ítems con filtros, obtener un ítem por ID y refrescar "
        "el almacén de datos subyacente. Usa el endpoint `admin/refresh` con "
        "la clave API correcta para re-ejecutar el proceso ETL."
    ),
    version="0.1.0",
)

@app.get("/items", response_model=List[ItemOut])
def list_items(
    *,
    q: Optional[str] = Query(None, description="Término de búsqueda para el título"),
    author: Optional[str] = Query(None, description="Filtrar por nombre de autor"),
    type: Optional[str] = Query(None, description="Filtrar por tipo/categoría"),
    genre: Optional[str] = Query(None, description="Filtrar por género/tema"),
    location: Optional[str] = Query(None, description="Filtrar por ubicación"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de resultados a devolver"),
    offset: int = Query(0, ge=0, description="Número de ítems a omitir"),
    session: Session = Depends(get_session),
) -> List[ItemOut]:
    """
    Lista ítems con búsqueda y filtrado opcional.

    Este endpoint soporta búsqueda de texto básica en el título así como
    filtrado por autor, tipo y ubicación. Los resultados se paginan vía
    los parámetros ``limit`` y ``offset``.
    """
    try:
        stmt = select(Item)
        if q:
            # Buscar en título o ubicación
            stmt = stmt.where(
                or_(
                    Item.title.ilike(f"%{q}%"),
                    Item.location.ilike(f"%{q}%")
                )
            )
        if author:
            stmt = stmt.where(Item.author.ilike(f"%{author}%"))
        if type:
            stmt = stmt.where(Item.type == type)
        if location:
            stmt = stmt.where(Item.location.ilike(f"%{location}%"))
        if genre:
            stmt = stmt.where(Item.genre.ilike(f"%{genre}%"))
        stmt = stmt.offset(offset).limit(limit)
        results = session.scalars(stmt).all()
        return [ItemOut.from_orm(obj) for obj in results]
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: str, session: Session = Depends(get_session)) -> ItemOut:
    """
    Recupera un ítem único por su ID.

    Lanza un error 404 si el ítem no existe.
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ítem no encontrado")
    return ItemOut.from_orm(item)

@app.post("/admin/refresh", status_code=status.HTTP_202_ACCEPTED)
def refresh(x_api_key: Optional[str] = Header(None, alias="X-API-KEY")) -> dict:
    """
    Refresca el conjunto de datos re-ejecutando el pipeline ETL.

    Este endpoint está protegido con una clave API simple. Para invocarlo, proporciona
    el header ``X-API-KEY`` con el valor de la variable de entorno ``API_KEY``.
    Se devuelve un código de estado ``202 Accepted`` inmediatamente; el proceso
    ETL se ejecuta síncronamente en esta implementación.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Clave API inválida")
    # Ejecutar el proceso ETL. Esta llamada es síncrona; para un sistema de producción
    # considera delegar a una tarea en segundo plano o cola de trabajo.
    etl_run()
    return {"status": "refresco iniciado"}

@app.get("/genres", response_model=List[GenreOut])
def list_genres(
    *,
    session: Session = Depends(get_session)
) -> List[GenreOut]:
    """
    Devuelve una lista de géneros/temas distintos con su conteo aproximado.

    Divide el campo ``genre`` (CSV) y normaliza a minúsculas.
    """
    stmt = select(Item.genre)
    rows = session.execute(stmt).all()
    counts: dict[str, int] = {}
    for (g,) in rows:
        if not g:
            continue
        parts = [p.strip().lower() for p in g.split(',') if p and p.strip()]
        for p in parts:
            counts[p] = counts.get(p, 0) + 1
    # construir respuesta ordenada por frecuencia desc
    entries = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return [GenreOut(name=name, count=count) for name, count in entries[:200]]