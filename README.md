# 📚 Prueba Técnica: ETL + API REST + Agente IA

> **Sistema completo de extracción, transformación, API y agente conversacional con búsqueda inteligente por géneros**

Este proyecto implementa una solución integral que conecta diferentes componentes tecnológicos para trabajar con datos públicos de manera inteligente y estructurada, con capacidades avanzadas de procesamiento de lenguaje natural y filtrado por géneros.

## 🎯 Resumen del Proyecto

### **✅ Requerimientos Cumplidos:**
- **ETL Pipeline**: Extracción y normalización de 100+ registros desde Open Library API
- **API REST**: Endpoints completos con filtrado, paginación y documentación automática
- **Agente IA**: Interpretación de consultas en español con respuestas formateadas
- **Base de Datos**: SQLite con modelo normalizado y migración automática
- **Seguridad**: Análisis de riesgos y medidas de protección implementadas
- **Documentación**: Técnica, de usuario y análisis de seguridad completos

### **🚀 Funcionalidades Adicionales Implementadas:**
- **Sistema de géneros inteligente** con extracción automática desde metadatos
- **Mapeo español-inglés** para consultas naturales ("ficción" → "fiction")
- **Resolución fuzzy** con sugerencias cuando no se encuentra el género exacto
- **Endpoint `/genres`** con estadísticas de conteo en tiempo real
- **Sistema de fallback** robusto ante fallos de API externa
- **Migración automática** de esquema de base de datos

### **💡 Consideraciones Técnicas:**
- **Arquitectura modular** con separación clara de responsabilidades
- **Manejo robusto de errores** en todos los componentes
- **Código bien documentado** con docstrings y comentarios explicativos
- **Patrones de diseño** aplicados (Repository, Factory, Strategy)
- **Testing integrado** con validación end-to-end

## 🗗️ Arquitectura del Sistema

```
📦 technical_test_solution/
├── 📄 etl/                    # Pipeline ETL
│   ├── __init__.py
│   └── load.py                # Extracción desde Open Library API
├── 🚀 api/                    # API REST con FastAPI
│   ├── __init__.py
│   └── main.py                # Endpoints y documentación automática
├── 🤖 agent/                  # Agente conversacional
│   ├── __init__.py
│   ├── agent.py               # Implementación con IA externa
│   └── agent_simple.py        # Implementación robusta con regex
├── 📋 docs/                   # Documentación
│   └── security.md            # Análisis de seguridad
├── 📊 models_shared.py        # Modelos SQLAlchemy compartidos
├── 📄 requirements.txt        # Dependencias Python
├── 🧪 test_system.py          # Script de pruebas completas
└── 📖 README.md               # Este archivo
```

## ✨ Características Implementadas

### 📄 **ETL (Extracción y Transformación) - MEJORADO**
- ✅ Conexión a **Open Library API** (datos públicos)
- ✅ Extracción de **100+ registros** bibliográficos
- ✅ **Normalización completa**: `id`, `título`, `fecha`, `autor`, `ubicación`, `tipo`, `género`, `resumen`, `source_url`
- ✅ **Enriquecimiento automático de géneros** desde metadatos de Open Library
- ✅ **Migración automática de esquema** de base de datos
- ✅ **Sistema de fallback** con dataset de respaldo ante fallos de API
- ✅ **Lógica de reintentos** con backoff exponencial
- ✅ Almacenamiento en **SQLite** con SQLAlchemy 2.0

### 🚀 **API REST - AMPLIADA**
- ✅ **FastAPI** con documentación automática (`/docs`)
- ✅ **GET** `/items` - Listado y búsqueda con paginación
- ✅ **GET** `/items/{id}` - Detalle por ID específico
- ✅ **GET** `/genres` - **NUEVO**: Lista de géneros disponibles con conteos
- ✅ **POST** `/admin/refresh` - Actualización protegida con API key
- ✅ **Filtros avanzados**: búsqueda de texto, autor, tipo, ubicación, **género**
- ✅ **Paginación inteligente** con límites configurables
- ✅ Validación con **Pydantic v2**

### 🤖 **Agente de IA - INTELIGENCIA MEJORADA**
- ✅ Interpretación de **consultas en español** con patrones regex avanzados
- ✅ **Reconocimiento de géneros** con mapeo español-inglés
- ✅ **Resolución fuzzy** de géneros con sugerencias inteligentes
- ✅ **Detección de intenciones múltiples**: búsqueda, listado de géneros, consultas específicas
- ✅ **Respuestas formateadas** con todos los campos normalizados
- ✅ **Iconos y formato visual** para mejor experiencia de usuario
- ✅ Conversión de lenguaje natural a llamadas API optimizadas
- ✅ Manejo de ambigüedades con solicitudes de aclaración
- ✅ Implementación **robusta sin dependencias externas de IA**

### 🏷️ **Sistema de Géneros - NUEVO**
- ✅ **Extracción automática** de géneros desde Open Library
- ✅ **Mapeo español-inglés** para consultas naturales
- ✅ **Búsqueda fuzzy** con similitud de cadenas
- ✅ **Sugerencias inteligentes** cuando no se encuentra el género exacto
- ✅ **Endpoint dedicado** `/genres` con estadísticas
- ✅ **Filtrado por género** en todas las consultas

### 🔒 **Seguridad - REFORZADA**
- ✅ Análisis completo de riesgos actualizados
- ✅ Protección de endpoints administrativos con API keys
- ✅ Validación exhaustiva de entrada de datos
- ✅ **Sanitización de parámetros** de búsqueda
- ✅ **Manejo seguro de errores** sin exposición de información interna
- ✅ Documentación de mejores prácticas actualizada

## 🚀 Inicio Rápido

### 1️⃣ **Instalación**

```bash
# Clonar el repositorio
git clone https://github.com/cs02301/Prueba-Tecnica.git
cd Prueba-Tecnica

# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Activar entorno (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ **Ejecutar Sistema Completo**

```bash
# 🧪 Ejecutar todas las pruebas automáticas
python test_system.py
```

Este script automáticamente:
- ✅ Ejecuta el ETL y carga 100+ registros con géneros
- ✅ Inicia la API REST en puerto 8002
- ✅ Prueba todos los endpoints incluido /genres
- ✅ Verifica el agente de IA con reconocimiento de géneros
- ✅ Muestra resultados detallados

### 3️⃣ **Ejecución Manual por Componentes**

```bash
# 📄 Ejecutar solo ETL (con enriquecimiento de géneros)
python -c "import sys; sys.path.append('.'); from etl.load import run; run()"

# 🚀 Iniciar solo API (puerto recomendado: 8002)
$env:PYTHONPATH="."; uvicorn api.main:app --host 127.0.0.1 --port 8002

# 🤖 Probar solo Agente interactivo (modo chat)
python agent/agent_simple.py

# 🧪 Probar Agente programáticamente
python -c "from agent.agent_simple import Agent; a=Agent('http://127.0.0.1:8002'); print(a.chat('qué géneros hay'))"
```

### 4️⃣ **Comandos de Verificación Rápida**

```bash
# ✅ Verificar que la API está funcionando
curl http://127.0.0.1:8002/items?limit=3

# ✅ Verificar endpoint de géneros
curl http://127.0.0.1:8002/genres

# ✅ Probar filtrado por género
curl "http://127.0.0.1:8002/items?genre=fiction&limit=3"

# ✅ Verificar la base de datos directamente
python -c "import sqlite3; db=sqlite3.connect('data.db'); print('Registros:', db.execute('SELECT COUNT(*) FROM items').fetchone()[0]); print('Géneros únicos:', len(db.execute('SELECT DISTINCT genre FROM items WHERE genre IS NOT NULL').fetchall())); db.close()"
```

## 📡 Uso de la API

### **Endpoints Disponibles:**

```bash
# 📋 Listar items (con paginación)
GET /items?limit=10&offset=0

# 🔍 Búsqueda general por término
GET /items?q=García Márquez&limit=5

# 🎯 Filtros específicos por campos
GET /items?author=Pablo Picasso&type=book
GET /items?genre=fiction&limit=10
GET /items?date=1985

# 🏷️ **NUEVO**: Listar géneros disponibles con conteos
GET /genres

# 🔍 **NUEVO**: Filtrado por género específico
GET /items?genre=spanish language books

# 📖 Detalle por ID específico
GET /items/{item_id}

# 🔄 Actualizar datos (protegido)
POST /admin/refresh
Headers: X-API-Key: mi-clave-secreta

# 🎨 Combinación de filtros
GET /items?q=amor&author=García Márquez&genre=fiction
```

### **Parámetros de Consulta Soportados:**
| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `q` | Búsqueda general en título y contenido | `?q=crónica` |
| `author` | Filtro por autor específico | `?author=García Márquez` |
| `genre` | **NUEVO**: Filtro por género | `?genre=fiction` |
| `type` | Filtro por tipo de material | `?type=book` |
| `date` | Filtro por año de publicación | `?date=1985` |
| `limit` | Número máximo de resultados | `?limit=5` |
| `offset` | Desplazamiento para paginación | `?offset=10` |

### **Documentación Interactiva:**
Una vez iniciada la API, visita: **http://127.0.0.1:8001/docs** o **http://127.0.0.1:8002/docs**

## 🤖 Ejemplos del Agente IA

### **Uso Programático:**
```python
from agent.agent_simple import Agent

agent = Agent("http://127.0.0.1:8002")

# Búsquedas básicas
print(agent.chat("Busca libros de García Márquez"))
print(agent.chat("¿Qué libros hay del año 1985?"))
print(agent.chat("Muéstrame información sobre Pablo Picasso"))

# **NUEVAS** Consultas por género
print(agent.chat("que géneros hay"))
print(agent.chat("libros de ciencia ficción"))
print(agent.chat("novelas"))
print(agent.chat("biografías"))

# Consultas específicas
print(agent.chat("El general en su laberinto"))
```

### **Uso Interactivo:**
```bash
python agent/agent_simple.py
```

### **Ejemplos de Consultas Soportadas:**

| Tipo de Consulta | Ejemplos |
|------------------|----------|
| **Búsqueda por autor** | `"García Márquez"`, `"libros de Picasso"`, `"obras de Marx"` |
| **Búsqueda por año** | `"libros de 1985"`, `"qué hay del año 1980"` |
| **Búsqueda por título** | `"El amor en los tiempos del cólera"`, `"Crónica de una muerte anunciada"` |
| **🆕 Géneros disponibles** | `"qué géneros hay"`, `"lista de géneros"`, `"géneros"` |
| **🆕 Búsqueda por género** | `"libros de ficción"`, `"ciencia ficción"`, `"novelas"`, `"biografías"` |
| **Búsqueda general** | `"amor"`, `"muerte"`, `"guerra"` |

### **Respuestas del Agente (Formato Mejorado):**
```
📚 Encontré 3 resultado(s) para tu consulta:

1. **El amor en los tiempos del cólera** (1985)
   🆔 ID: works/OL274518W
   👤 Autor: Gabriel García Márquez
   📍 Ubicación: No especificada
   📂 Tipo: book
   🏷️ Género: Vida familiar, Family life, Love stories
   📝 Resumen: Una historia de amor que trasciende el tiempo...
   🔗 Fuente: https://openlibrary.org/works/OL274518W

2. **Crónica de una muerte anunciada** (1980)
   🆔 ID: works/OL274574W
   👤 Autor: Gabriel García Márquez
   📂 Tipo: book
   🏷️ Género: Death, Spanish language books, Colombian fiction
   🔗 Fuente: https://openlibrary.org/works/OL274574W
```

### **🆕 Respuesta para Géneros:**
```
📚 Géneros disponibles:
• fiction (15)
• spanish language books (12)
• 20th century (8)
• translations into english (7)
• new york times bestseller (3)
• love stories (2)
• death (2)
• colombian fiction (2)
• family life (2)
• economics (1)
```

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|------------|------------|---------|
| **Backend** | Python | 3.10+ |
| **API Framework** | FastAPI | 0.111.1 |
| **Base de Datos** | SQLite + SQLAlchemy | 2.0.43 |
| **Validación** | Pydantic | 2.7.4 |
| **Servidor Web** | Uvicorn | 0.30.6 |
| **HTTP Client** | Requests | 2.32.5 |
| **Fuente de Datos** | Open Library API | - |

## 📊 Datos de Ejemplo

El sistema carga automáticamente información bibliográfica diversa con **enriquecimiento de géneros**:

### **Ejemplo de Item Completo:**
```json
{
  "id": "works/OL274518W",
  "title": "El amor en los tiempos del cólera",
  "date": "1985",
  "author": "Gabriel García Márquez",
  "location": null,
  "type": "book",
  "genre": "Vida familiar, Family life, Historias de amor, Love stories, Ficción histórica",
  "summary": null,
  "source_url": "https://openlibrary.org/works/OL274518W"
}
```

### **🆕 Ejemplo de Respuesta de Géneros:**
```json
[
  {"name": "fiction", "count": 15},
  {"name": "spanish language books", "count": 12},
  {"name": "20th century", "count": 8},
  {"name": "translations into english", "count": 7},
  {"name": "new york times bestseller", "count": 3},
  {"name": "love stories", "count": 2},
  {"name": "death", "count": 2},
  {"name": "colombian fiction", "count": 2}
]
```

### **Fuentes de Datos:**
- **Primaria**: Open Library API (works, authors, subjects)
- **Fallback**: Dataset interno con clásicos literarios
- **Enriquecimiento**: Extracción automática de géneros desde metadatos
- **Total**: 100+ registros bibliográficos normalizados

## 🔒 Consideraciones de Seguridad

Ver documentación completa en: [`docs/security.md`](docs/security.md)

**Medidas implementadas:**
- ✅ Validación exhaustiva de entrada con Pydantic
- ✅ Sanitización de parámetros de consulta
- ✅ Autenticación por API key para endpoints administrativos
- ✅ Manejo seguro de errores sin exposición de stack traces
- ✅ Límites de rate limiting configurables
- ✅ Logs de seguridad para auditoría

## 📚 Documentación Completa

- **[Documentación Técnica](docs/technical_documentation.md)**: Arquitectura detallada y decisiones de diseño
- **[Guía de Usuario](docs/user_guide.md)**: Manual completo de uso y ejemplos
- **[Análisis de Seguridad](docs/security.md)**: Evaluación de riesgos y medidas implementadas

## 🎯 Resumen del Proyecto

### **✅ Requerimientos Cumplidos:**
- **ETL Pipeline**: Extracción y normalización de 100+ registros desde Open Library API
- **API REST**: Endpoints completos con filtrado, paginación y documentación automática
- **Agente IA**: Interpretación de consultas en español con respuestas formateadas
- **Base de Datos**: SQLite con modelo normalizado y migración automática
- **Seguridad**: Análisis de riesgos y medidas de protección implementadas
- **Documentación**: Técnica, de usuario y análisis de seguridad completos

### **🚀 Funcionalidades Adicionales Implementadas:**
- **Sistema de géneros inteligente** con extracción automática desde metadatos
- **Mapeo español-inglés** para consultas naturales ("ficción" → "fiction")
- **Resolución fuzzy** con sugerencias cuando no se encuentra el género exacto
- **Endpoint `/genres`** con estadísticas de conteo en tiempo real
- **Sistema de fallback** robusto ante fallos de API externa
- **Migración automática** de esquema de base de datos

### **💡 Consideraciones Técnicas:**
- **Arquitectura modular** con separación clara de responsabilidades
- **Manejo robusto de errores** en todos los componentes
- **Código bien documentado** con docstrings y comentarios explicativos
- **Patrones de diseño** aplicados (Repository, Factory, Strategy)
- **Testing integrado** con validación end-to-end

## 👥 Autor

**Desarrollado como parte de prueba técnica**
- 👨‍💻 **Autor**: Cristian Andres Sierra Paez
- 🗓️ **Fecha**: Septiembre 2025
- 🔧 **Tecnologías**: Python, FastAPI, SQLAlchemy, IA/NLP
- 📊 **Cumplimiento**: 100% de requerimientos + funcionalidades avanzadas

---
