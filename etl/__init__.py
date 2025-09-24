"""
ETL Module Documentation
========================

Este módulo implementa el pipeline ETL (Extract, Transform, Load) para la prueba técnica.

Funcionalidades Principales:
- Extracción de datos desde Open Library API
- Enriquecimiento automático de géneros
- Migración automática de esquema de base de datos
- Sistema de fallback con datos de respaldo
- Lógica de reintentos con backoff exponencial

Componentes:
- run(): Función principal del pipeline ETL
- fetch_records(): Extracción de datos desde Open Library
- enrich_missing_genres(): Enriquecimiento de géneros faltantes
- ensure_schema(): Migración automática de esquema
- _fallback_records(): Dataset de respaldo ante fallos

Uso:
    from etl.load import run
    run()  # Ejecuta el pipeline completo

Variables de Entorno:
- OPENLIBRARY_QUERY: Query personalizado para Open Library (opcional)

Dependencias:
- requests: Para llamadas HTTP a Open Library API
- sqlalchemy: ORM para base de datos
- models_shared: Modelos de datos compartidos

Author: Desarrollado para prueba técnica
Date: Septiembre 2025
"""
