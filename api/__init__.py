"""
API Module Documentation
=========================

Este módulo implementa la API REST con FastAPI para la prueba técnica.

Funcionalidades Principales:
- API REST completa con FastAPI
- Endpoints para búsqueda y filtrado de items
- Endpoint dedicado para listado de géneros
- Validación de datos con Pydantic v2
- Documentación automática con Swagger UI
- Paginación inteligente
- Filtrado por múltiples criterios

Endpoints Principales:
- GET /items: Listado y búsqueda con filtros
- GET /items/{id}: Consulta por ID específico
- GET /genres: Lista de géneros disponibles con conteos
- POST /admin/refresh: Actualización de datos (protegido)

Filtros Soportados:
- q: Búsqueda general en título y contenido
- author: Filtro por autor específico
- genre: Filtro por género
- type: Filtro por tipo de material
- date: Filtro por año de publicación
- limit/offset: Paginación

Uso:
    uvicorn api.main:app --host 127.0.0.1 --port 8002

Documentación:
    http://127.0.0.1:8002/docs (Swagger UI)
    http://127.0.0.1:8002/redoc (ReDoc)

Author: Desarrollado para prueba técnica
Date: Septiembre 2025
"""
