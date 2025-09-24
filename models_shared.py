"""
Modelos SQLAlchemy compartidos para la aplicación de prueba técnica.

Este módulo define una clase base declarativa y un modelo ``Item`` usado
tanto por la capa ETL como por la capa API. Mantener la definición del modelo
en un solo lugar evita duplicación y asegura que el esquema de base de datos
se mantenga consistente a través del proyecto.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text

class Base(DeclarativeBase):
    """Clase base para todos los modelos declarativos."""
    pass

class Item(Base):
    """
    Representación normalizada de un registro público.

    Attributes
    ----------
    id : str
        Primary key of the item. Depending on the upstream source this
        could be a natural key or a synthetic identifier.
    title : str
        Human–readable title of the item.
    date : str | None
        Publication date in ISO 8601 ``YYYY-MM-DD`` format where possible.
    author : str | None
        Name of the author or responsible entity.
    location : str | None
        Geographic location associated with the item.
    type : str | None
        Category or type for the item, for example “book” or “report”.
    summary : str | None
        Short free‑form summary or description of the item.
    source_url : str | None
        Original URL to the item in the source system.
    genre : str | None
        A comma-separated list of subjects/genres for the item, if available.
    """
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    date: Mapped[str | None] = mapped_column(String, index=True)
    author: Mapped[str | None] = mapped_column(String, index=True)
    location: Mapped[str | None] = mapped_column(String, index=True)
    type: Mapped[str | None] = mapped_column(String, index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(String)
    genre: Mapped[str | None] = mapped_column(String, index=True)

    def __repr__(self) -> str:
        return (
            f"<Item id={self.id!r} title={self.title!r} date={self.date!r} "
            f"author={self.author!r} genre={self.genre!r}>"
        )