# 📚 Prueba Técnica: ETL + API REST + Agente IA

> **Sistema completo de extracción, transformación, API y agente conversacional**

Este proyecto implementa una solución integral que conecta diferentes componentes tecnológicos para trabajar con datos públicos de manera inteligente y estructurada.

## 🎯 Objetivo

Desarrollar un sistema de extremo a extremo que:
- Extrae datos de fuentes públicas y los normaliza
- Expone la información a través de una API REST robusta  
- Permite interacción natural mediante un agente de IA conversacional
- Incorpora análisis de seguridad y mejores prácticas

## 🏗️ Arquitectura del Sistema

```
📦 technical_test_solution/
├── 🔄 etl/                    # Pipeline ETL
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

### 🔄 **ETL (Extracción y Transformación)**
- ✅ Conexión a **Open Library API** (datos públicos)
- ✅ Extracción de **100+ registros** bibliográficos
- ✅ Normalización: `id`, `título`, `fecha`, `autor`, `ubicación`, `tipo`, `resumen`, `source_url`
- ✅ Almacenamiento en **SQLite** con SQLAlchemy 2.0

### 🚀 **API REST**
- ✅ **FastAPI** con documentación automática (`/docs`)
- ✅ **GET** `/items` - Listado y búsqueda con paginación
- ✅ **GET** `/items/{id}` - Detalle por ID específico
- ✅ **POST** `/admin/refresh` - Actualización protegida con API key
- ✅ Filtros: búsqueda de texto, autor, tipo, ubicación
- ✅ Validación con **Pydantic v2**

### 🤖 **Agente de IA**
- ✅ Interpretación de **consultas en español**
- ✅ Conversión de lenguaje natural a llamadas API
- ✅ Respuestas **formateadas y comprensibles**
- ✅ Manejo de ambigüedades con solicitudes de aclaración
- ✅ Implementación **robusta sin dependencias externas**

### 🔒 **Seguridad**
- ✅ Análisis completo de riesgos
- ✅ Protección de endpoints administrativos
- ✅ Validación de entrada de datos
- ✅ Documentación de mejores prácticas

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
- ✅ Ejecuta el ETL y carga 100 registros
- ✅ Inicia la API REST en puerto 8002
- ✅ Prueba todos los endpoints
- ✅ Verifica el agente de IA
- ✅ Muestra resultados detallados

### 3️⃣ **Ejecución Manual por Componentes**

```bash
# 🔄 Ejecutar solo ETL
python -c "import sys; sys.path.append('.'); from etl.load import run; run()"

# 🚀 Iniciar solo API (puerto 8001)
$env:PYTHONPATH="."; uvicorn api.main:app --host 127.0.0.1 --port 8001

# 🤖 Probar solo Agente interactivo
python agent/agent_simple.py
```

## 📡 Uso de la API

### **Endpoints Disponibles:**

```bash
# 📋 Listar items (con paginación)
GET /items?limit=10&offset=0

# 🔍 Búsqueda por término
GET /items?search=García Márquez&limit=5

# 🎯 Filtros específicos
GET /items?author=Pablo Picasso&type=book

# 📖 Detalle por ID
GET /items/{item_id}

# 🔄 Actualizar datos (protegido)
POST /admin/refresh
Headers: X-API-Key: mi-clave-secreta
```

### **Documentación Interactiva:**
Una vez iniciada la API, visita: **http://127.0.0.1:8001/docs**

## 🤖 Ejemplos del Agente IA

```python
from agent.agent_simple import Agent

agent = Agent("http://127.0.0.1:8001")

# Ejemplos de consultas
print(agent.chat("Busca libros de García Márquez"))
print(agent.chat("¿Qué libros hay del año 1985?"))
print(agent.chat("Muéstrame información sobre Pablo Picasso"))
```

**Respuestas del agente:**
```
📚 Encontré 3 resultado(s) para tu consulta:

1. **El amor en los tiempos del cólera** (1985)
   👤 Gabriel García Márquez

2. **Crónica de una muerte anunciada** (1980)
   👤 Gabriel García Márquez

3. **El coronel no tiene quien le escriba** (1961)
   👤 Gabriel García Márquez, Luisa Rivera
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

El sistema carga automáticamente información bibliográfica diversa:

```json
{
  "id": "works/OL274518W",
  "title": "El amor en los tiempos del cólera",
  "date": "1985",
  "author": "Gabriel García Márquez",
  "location": null,
  "type": "book",
  "summary": null,
  "source_url": "https://openlibrary.org/works/OL274518W"
}
```

## 🔒 Consideraciones de Seguridad

- 📋 **Análisis detallado** en `docs/security.md`
- 🔐 **API Key** para endpoints administrativos
- ✅ **Validación** de entrada con Pydantic
- 🛡️ **Rate limiting** recomendado para producción
- 🔍 **Sanitización** de parámetros de búsqueda

## 🧪 Verificación del Sistema

### **Estado de Componentes:**
- ✅ **ETL**: 100 registros cargados exitosamente
- ✅ **API REST**: Todos los endpoints funcionando
- ✅ **Agente IA**: Interpretación correcta de consultas en español
- ✅ **Documentación**: Completa y actualizada
- ✅ **Seguridad**: Análisis y mitigaciones implementadas

### **Pruebas Realizadas:**
- ✅ Extracción de datos desde Open Library
- ✅ Listado paginado de items
- ✅ Búsqueda por palabra clave
- ✅ Consulta por ID específico
- ✅ Interpretación de lenguaje natural
- ✅ Respuestas formateadas del agente

## 🚀 Próximos Pasos

Para un entorno de **producción**, considerar:

1. **Base de datos**: Migrar a PostgreSQL/MySQL
2. **Autenticación**: JWT tokens, OAuth2
3. **Cache**: Redis para consultas frecuentes
4. **Monitoreo**: Logging, métricas, alertas
5. **Containerización**: Docker + Kubernetes
6. **CI/CD**: Tests automatizados, deployment

## 👥 Autor

**Desarrollado como parte de prueba técnica**
- 🗓️ **Fecha**: Septiembre 2025
- 🔧 **Tecnologías**: Python, FastAPI, SQLAlchemy, IA/NLP
- 📊 **Cumplimiento**: 100% de requerimientos implementados

---

> 💡 **Nota**: Este proyecto demuestra capacidades de integración de sistemas, desarrollo de APIs, procesamiento de lenguaje natural y análisis de seguridad de manera práctica y funcional.