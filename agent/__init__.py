"""
Agent Module Documentation
===========================

Este módulo implementa el agente conversacional de IA para la prueba técnica.

Funcionalidades Principales:
- Interpretación de consultas en lenguaje natural (español)
- Reconocimiento de intenciones con patrones regex avanzados
- Mapeo de géneros español-inglés
- Resolución fuzzy de géneros con sugerencias
- Conversión de lenguaje natural a llamadas API
- Respuestas formateadas con todos los campos normalizados

Agentes Disponibles:
- agent_simple.py: Implementación robusta sin dependencias de IA externa
- agent.py: Implementación con servicios de IA externos (OpenAI)
- agent_fixed.py: Versión experimental

Tipos de Consultas Soportadas:
- Búsqueda por autor: "García Márquez", "libros de Picasso"
- Búsqueda por año: "libros de 1985", "qué hay del año 1980"
- Búsqueda por título: "El amor en los tiempos del cólera"
- Listado de géneros: "qué géneros hay", "géneros disponibles"
- Búsqueda por género: "libros de ficción", "ciencia ficción", "novelas"
- Búsqueda general: "amor", "muerte", "guerra"

Uso Interactivo:
    python agent/agent_simple.py

Uso Programático:
    from agent.agent_simple import Agent
    agent = Agent("http://127.0.0.1:8002")
    response = agent.chat("qué géneros hay")

Características Avanzadas:
- Detección de intenciones múltiples
- Mapeo inteligente de géneros
- Sugerencias cuando no se encuentra género exacto
- Formato de respuesta con iconos y estructura clara
- Manejo robusto de errores

Author: Desarrollado para prueba técnica
Date: Septiembre 2025
"""
