# ðŸ“š Prueba TÃ©cnica: ETL + API REST + Agente IA

> **Sistema completo de extracciÃ³n, transformaciÃ³n, API y agente conversacional con bÃºsqueda inteligente por gÃ©neros**

Este proyecto implementa una soluciÃ³n integral que conecta diferentes componentes tecnolÃ³gicos para trabajar con datos pÃºblicos de manera inteligente y estructurada, con capacidades avanzadas - âœ… **Formato de respuesta mejorado** con iconos y estructura clara

## ðŸŽ¯ Resumen del Proyecto

### **âœ… Requerimientos Cumplidos:**
- **ETL Pipeline**: ExtracciÃ³n y normalizaciÃ³n de 100+ registros desde Open Library API
- **API REST**: Endpoints completos con filtrado, paginaciÃ³n y documentaciÃ³n automÃ¡tica
- **Agente IA**: InterpretaciÃ³n de consultas en espaÃ±ol con respuestas formateadas
- **Base de Datos**: SQLite con modelo normalizado y migraciÃ³n automÃ¡tica
- **Seguridad**: AnÃ¡lisis de riesgos y medidas de protecciÃ³n implementadas
- **DocumentaciÃ³n**: TÃ©cnica, de usuario y anÃ¡lisis de seguridad completos

### **ðŸš€ Funcionalidades Adicionales Implementadas:**
- **Sistema de gÃ©neros inteligente** con extracciÃ³n automÃ¡tica desde metadatos
- **Mapeo espaÃ±ol-inglÃ©s** para consultas naturales ("ficciÃ³n" â†’ "fiction")
- **ResoluciÃ³n fuzzy** con sugerencias cuando no se encuentra el gÃ©nero exacto
- **Endpoint `/genres`** con estadÃ­sticas de conteo en tiempo real
- **Sistema de fallback** robusto ante fallos de API externa
- **MigraciÃ³n automÃ¡tica** de esquema de base de datos

### **ðŸ’¡ Consideraciones TÃ©cnicas:**
- **Arquitectura modular** con separaciÃ³n clara de responsabilidades
- **Manejo robusto de errores** en todos los componentes
- **CÃ³digo bien documentado** con docstrings y comentarios explicativos
- **Patrones de diseÃ±o** aplicados (Repository, Factory, Strategy)
- **Testing integrado** con validaciÃ³n end-to-end

## ðŸ‘¥ Autor

**Desarrollado como parte de prueba tÃ©cnica**
- ðŸ‘¨â€ðŸ’» **Autor**: Cristian Andres Sierra Paez
- ðŸ—“ï¸ **Fecha**: Septiembre 2025
- ðŸ”§ **TecnologÃ­as**: Python, FastAPI, SQLAlchemy, IA/NLP
- ðŸ“Š **Cumplimiento**: 100% de requerimientos + funcionalidades avanzadas

---

> ðŸ’¡ **Este proyecto demuestra capacidades de integraciÃ³n de sistemas, desarrollo de APIs, procesamiento de lenguaje natural y anÃ¡lisis de seguridad de manera prÃ¡ctica y funcional.**ocesamiento de lenguaje natural y filtrado por gÃ©neros.

## ðŸŽ¯ Objetivo

Desarrollar un sistema de extremo a extremo que:
- Extrae datos de fuentes pÃºblicas y los normaliza con **enriquecimiento automÃ¡tico de gÃ©neros**
- Expone la informaciÃ³n a travÃ©s de una API REST robusta con **filtrado avanzado**
- Permite interacciÃ³n natural mediante un agente de IA conversacional con **reconocimiento de gÃ©neros en espaÃ±ol**
- Incorpora anÃ¡lisis de seguridad y mejores prÃ¡cticas
- Maneja **fallback de datos** y **recuperaciÃ³n automÃ¡tica** ante fallos de API

## ðŸ—ï¸ Arquitectura del Sistema

```
ðŸ“¦ technical_test_solution/
â”œâ”€â”€ ðŸ”„ etl/                    # Pipeline ETL
â”‚   â”œâ”€â”€ __init__.py
â”‚   â””â”€â”€ load.py                # ExtracciÃ³n desde Open Library API
â”œâ”€â”€ ðŸš€ api/                    # API REST con FastAPI
â”‚   â”œâ”€â”€ __init__.py
â”‚   â””â”€â”€ main.py                # Endpoints y documentaciÃ³n automÃ¡tica
â”œâ”€â”€ ðŸ¤– agent/                  # Agente conversacional
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ agent.py               # ImplementaciÃ³n con IA externa
â”‚   â””â”€â”€ agent_simple.py        # ImplementaciÃ³n robusta con regex
â”œâ”€â”€ ðŸ“‹ docs/                   # DocumentaciÃ³n
â”‚   â””â”€â”€ security.md            # AnÃ¡lisis de seguridad
â”œâ”€â”€ ðŸ“Š models_shared.py        # Modelos SQLAlchemy compartidos
â”œâ”€â”€ ðŸ“„ requirements.txt        # Dependencias Python
â”œâ”€â”€ ðŸ§ª test_system.py          # Script de pruebas completas
â””â”€â”€ ðŸ“– README.md               # Este archivo
```

## âœ¨ CaracterÃ­sticas Implementadas

### ðŸ”„ **ETL (ExtracciÃ³n y TransformaciÃ³n) - MEJORADO**
- âœ… ConexiÃ³n a **Open Library API** (datos pÃºblicos)
- âœ… ExtracciÃ³n de **100+ registros** bibliogrÃ¡ficos
- âœ… **NormalizaciÃ³n completa**: `id`, `tÃ­tulo`, `fecha`, `autor`, `ubicaciÃ³n`, `tipo`, `gÃ©nero`, `resumen`, `source_url`
- âœ… **Enriquecimiento automÃ¡tico de gÃ©neros** desde metadatos de Open Library
- âœ… **MigraciÃ³n automÃ¡tica de esquema** de base de datos
- âœ… **Sistema de fallback** con dataset de respaldo ante fallos de API
- âœ… **LÃ³gica de reintentos** con backoff exponencial
- âœ… Almacenamiento en **SQLite** con SQLAlchemy 2.0

### ðŸš€ **API REST - AMPLIADA**
- âœ… **FastAPI** con documentaciÃ³n automÃ¡tica (`/docs`)
- âœ… **GET** `/items` - Listado y bÃºsqueda con paginaciÃ³n
- âœ… **GET** `/items/{id}` - Detalle por ID especÃ­fico
- âœ… **GET** `/genres` - **NUEVO**: Lista de gÃ©neros disponibles con conteos
- âœ… **POST** `/admin/refresh` - ActualizaciÃ³n protegida con API key
- âœ… **Filtros avanzados**: bÃºsqueda de texto, autor, tipo, ubicaciÃ³n, **gÃ©nero**
- âœ… **PaginaciÃ³n inteligente** con lÃ­mites configurables
- âœ… ValidaciÃ³n con **Pydantic v2**

### ðŸ¤– **Agente de IA - INTELIGENCIA MEJORADA**
- âœ… InterpretaciÃ³n de **consultas en espaÃ±ol** con patrones regex avanzados
- âœ… **Reconocimiento de gÃ©neros** con mapeo espaÃ±ol-inglÃ©s
- âœ… **ResoluciÃ³n fuzzy** de gÃ©neros con sugerencias inteligentes
- âœ… **DetecciÃ³n de intenciones mÃºltiples**: bÃºsqueda, listado de gÃ©neros, consultas especÃ­ficas
- âœ… **Respuestas formateadas** con todos los campos normalizados
- âœ… **Iconos y formato visual** para mejor experiencia de usuario
- âœ… ConversiÃ³n de lenguaje natural a llamadas API optimizadas
- âœ… Manejo de ambigÃ¼edades con solicitudes de aclaraciÃ³n
- âœ… ImplementaciÃ³n **robusta sin dependencias externas de IA**

### ðŸ·ï¸ **Sistema de GÃ©neros - NUEVO**
- âœ… **ExtracciÃ³n automÃ¡tica** de gÃ©neros desde Open Library
- âœ… **Mapeo espaÃ±ol-inglÃ©s** para consultas naturales
- âœ… **BÃºsqueda fuzzy** con similitud de cadenas
- âœ… **Sugerencias inteligentes** cuando no se encuentra el gÃ©nero exacto
- âœ… **Endpoint dedicado** `/genres` con estadÃ­sticas
- âœ… **Filtrado por gÃ©nero** en todas las consultas

### ðŸ”’ **Seguridad - REFORZADA**
- âœ… AnÃ¡lisis completo de riesgos actualizados
- âœ… ProtecciÃ³n de endpoints administrativos con API keys
- âœ… ValidaciÃ³n exhaustiva de entrada de datos
- âœ… **SanitizaciÃ³n de parÃ¡metros** de bÃºsqueda
- âœ… **Manejo seguro de errores** sin exposiciÃ³n de informaciÃ³n interna
- âœ… DocumentaciÃ³n de mejores prÃ¡cticas actualizada

## ðŸš€ Inicio RÃ¡pido

### 1ï¸âƒ£ **InstalaciÃ³n**

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

### 2ï¸âƒ£ **Ejecutar Sistema Completo**

```bash
# ðŸ§ª Ejecutar todas las pruebas automÃ¡ticas
python test_system.py
```

Este script automÃ¡ticamente:
- âœ… Ejecuta el ETL y carga 100+ registros con gÃ©neros
- âœ… Inicia la API REST en puerto 8002
- âœ… Prueba todos los endpoints incluido /genres
- âœ… Verifica el agente de IA con reconocimiento de gÃ©neros
- âœ… Muestra resultados detallados

### 3ï¸âƒ£ **EjecuciÃ³n Manual por Componentes**

```bash
# ðŸ”„ Ejecutar solo ETL (con enriquecimiento de gÃ©neros)
python -c "import sys; sys.path.append('.'); from etl.load import run; run()"

# ðŸš€ Iniciar solo API (puerto recomendado: 8002)
$env:PYTHONPATH="."; uvicorn api.main:app --host 127.0.0.1 --port 8002

# ðŸ¤– Probar solo Agente interactivo (modo chat)
python agent/agent_simple.py

# ðŸ§ª Probar Agente programÃ¡ticamente
python -c "from agent.agent_simple import Agent; a=Agent('http://127.0.0.1:8002'); print(a.chat('quÃ© gÃ©neros hay'))"
```

### 4ï¸âƒ£ **Comandos de VerificaciÃ³n RÃ¡pida**

```bash
# âœ… Verificar que la API estÃ¡ funcionando
curl http://127.0.0.1:8002/items?limit=3

# âœ… Verificar endpoint de gÃ©neros
curl http://127.0.0.1:8002/genres

# âœ… Probar filtrado por gÃ©nero
curl "http://127.0.0.1:8002/items?genre=fiction&limit=3"

# âœ… Verificar la base de datos directamente
python -c "import sqlite3; db=sqlite3.connect('data.db'); print('Registros:', db.execute('SELECT COUNT(*) FROM items').fetchone()[0]); print('GÃ©neros Ãºnicos:', len(db.execute('SELECT DISTINCT genre FROM items WHERE genre IS NOT NULL').fetchall())); db.close()"
```

## ðŸ“¡ Uso de la API

### **Endpoints Disponibles:**

```bash
# ðŸ“‹ Listar items (con paginaciÃ³n)
GET /items?limit=10&offset=0

# ðŸ” BÃºsqueda general por tÃ©rmino
GET /items?q=GarcÃ­a MÃ¡rquez&limit=5

# ðŸŽ¯ Filtros especÃ­ficos por campos
GET /items?author=Pablo Picasso&type=book
GET /items?genre=fiction&limit=10
GET /items?date=1985

# ðŸ·ï¸ **NUEVO**: Listar gÃ©neros disponibles con conteos
GET /genres

# ðŸ” **NUEVO**: Filtrado por gÃ©nero especÃ­fico
GET /items?genre=spanish language books

# ðŸ“– Detalle por ID especÃ­fico
GET /items/{item_id}

# ðŸ”„ Actualizar datos (protegido)
POST /admin/refresh
Headers: X-API-Key: mi-clave-secreta

# ðŸŽ¨ CombinaciÃ³n de filtros
GET /items?q=amor&author=GarcÃ­a MÃ¡rquez&genre=fiction
```

### **ParÃ¡metros de Consulta Soportados:**
| ParÃ¡metro | DescripciÃ³n | Ejemplo |
|-----------|-------------|---------|
| `q` | BÃºsqueda general en tÃ­tulo y contenido | `?q=crÃ³nica` |
| `author` | Filtro por autor especÃ­fico | `?author=GarcÃ­a MÃ¡rquez` |
| `genre` | **NUEVO**: Filtro por gÃ©nero | `?genre=fiction` |
| `type` | Filtro por tipo de material | `?type=book` |
| `date` | Filtro por aÃ±o de publicaciÃ³n | `?date=1985` |
| `limit` | NÃºmero mÃ¡ximo de resultados | `?limit=5` |
| `offset` | Desplazamiento para paginaciÃ³n | `?offset=10` |

### **DocumentaciÃ³n Interactiva:**
Una vez iniciada la API, visita: **http://127.0.0.1:8001/docs** o **http://127.0.0.1:8002/docs**

## ðŸ¤– Ejemplos del Agente IA

### **Uso ProgramÃ¡tico:**
```python
from agent.agent_simple import Agent

agent = Agent("http://127.0.0.1:8002")

# BÃºsquedas bÃ¡sicas
print(agent.chat("Busca libros de GarcÃ­a MÃ¡rquez"))
print(agent.chat("Â¿QuÃ© libros hay del aÃ±o 1985?"))
print(agent.chat("MuÃ©strame informaciÃ³n sobre Pablo Picasso"))

# **NUEVAS** Consultas por gÃ©nero
print(agent.chat("que gÃ©neros hay"))
print(agent.chat("libros de ciencia ficciÃ³n"))
print(agent.chat("novelas"))
print(agent.chat("biografÃ­as"))

# Consultas especÃ­ficas
print(agent.chat("El general en su laberinto"))
```

### **Uso Interactivo:**
```bash
python agent/agent_simple.py
```

### **Ejemplos de Consultas Soportadas:**

| Tipo de Consulta | Ejemplos |
|------------------|----------|
| **BÃºsqueda por autor** | `"GarcÃ­a MÃ¡rquez"`, `"libros de Picasso"`, `"obras de Marx"` |
| **BÃºsqueda por aÃ±o** | `"libros de 1985"`, `"quÃ© hay del aÃ±o 1980"` |
| **BÃºsqueda por tÃ­tulo** | `"El amor en los tiempos del cÃ³lera"`, `"CrÃ³nica de una muerte anunciada"` |
| **ðŸ†• GÃ©neros disponibles** | `"quÃ© gÃ©neros hay"`, `"lista de gÃ©neros"`, `"gÃ©neros"` |
| **ðŸ†• BÃºsqueda por gÃ©nero** | `"libros de ficciÃ³n"`, `"ciencia ficciÃ³n"`, `"novelas"`, `"biografÃ­as"` |
| **BÃºsqueda general** | `"amor"`, `"muerte"`, `"guerra"` |

### **Respuestas del Agente (Formato Mejorado):**
```
ðŸ“š EncontrÃ© 3 resultado(s) para tu consulta:

1. **El amor en los tiempos del cÃ³lera** (1985)
   ðŸ†” ID: works/OL274518W
   ðŸ‘¤ Autor: Gabriel GarcÃ­a MÃ¡rquez
   ðŸ“ UbicaciÃ³n: No especificada
   ðŸ“‚ Tipo: book
   ðŸ·ï¸ GÃ©nero: Vida familiar, Family life, Love stories
   ðŸ“ Resumen: Una historia de amor que trasciende el tiempo...
   ðŸ”— Fuente: https://openlibrary.org/works/OL274518W

2. **CrÃ³nica de una muerte anunciada** (1980)
   ðŸ†” ID: works/OL274574W
   ðŸ‘¤ Autor: Gabriel GarcÃ­a MÃ¡rquez
   ðŸ“‚ Tipo: book
   ðŸ·ï¸ GÃ©nero: Death, Spanish language books, Colombian fiction
   ðŸ”— Fuente: https://openlibrary.org/works/OL274574W
```

### **ðŸ†• Respuesta para GÃ©neros:**
```
ðŸ“š GÃ©neros disponibles:
â€¢ fiction (15)
â€¢ spanish language books (12)
â€¢ 20th century (8)
â€¢ translations into english (7)
â€¢ new york times bestseller (3)
â€¢ love stories (2)
â€¢ death (2)
â€¢ colombian fiction (2)
â€¢ family life (2)
â€¢ economics (1)
```

## ðŸ› ï¸ TecnologÃ­as Utilizadas

| Componente | TecnologÃ­a | VersiÃ³n |
|------------|------------|---------|
| **Backend** | Python | 3.10+ |
| **API Framework** | FastAPI | 0.111.1 |
| **Base de Datos** | SQLite + SQLAlchemy | 2.0.43 |
| **ValidaciÃ³n** | Pydantic | 2.7.4 |
| **Servidor Web** | Uvicorn | 0.30.6 |
| **HTTP Client** | Requests | 2.32.5 |
| **Fuente de Datos** | Open Library API | - |

## ðŸ“Š Datos de Ejemplo

El sistema carga automÃ¡ticamente informaciÃ³n bibliogrÃ¡fica diversa con **enriquecimiento de gÃ©neros**:

### **Ejemplo de Item Completo:**
```json
{
  "id": "works/OL274518W",
  "title": "El amor en los tiempos del cÃ³lera",
  "date": "1985",
  "author": "Gabriel GarcÃ­a MÃ¡rquez",
  "location": null,
  "type": "book",
  "genre": "Vida familiar, Family life, Historias de amor, Love stories, FicciÃ³ histÃ³rica",
  "summary": null,
  "source_url": "https://openlibrary.org/works/OL274518W"
}
```

### **ðŸ†• Ejemplo de Respuesta de GÃ©neros:**
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
- **Fallback**: Dataset interno con clÃ¡sicos literarios
- **Enriquecimiento**: ExtracciÃ³n automÃ¡tica de gÃ©neros desde metadatos
- **Total**: 100+ registros bibliogrÃ¡ficos normalizados

## ðŸ”’ Consideraciones de Seguridad


##  Resumen del Proyecto

### ** Requerimientos Cumplidos:**
- **ETL Pipeline**: Extracción y normalización de 100+ registros desde Open Library API
- **API REST**: Endpoints completos con filtrado, paginación y documentación automática
- **Agente IA**: Interpretación de consultas en español con respuestas formateadas
- **Base de Datos**: SQLite con modelo normalizado y migración automática
- **Seguridad**: Análisis de riesgos y medidas de protección implementadas
- **Documentación**: Técnica, de usuario y análisis de seguridad completos

### ** Funcionalidades Adicionales Implementadas:**
- **Sistema de géneros inteligente** con extracción automática desde metadatos
- **Mapeo español-inglés** para consultas naturales ("ficción"  "fiction")
- **Resolución fuzzy** con sugerencias cuando no se encuentra el género exacto
- **Endpoint `/genres` con estadísticas de conteo en tiempo real
- **Sistema de fallback** robusto ante fallos de API externa
- **Migración automática** de esquema de base de datos

### ** Consideraciones Técnicas:**
- **Arquitectura modular** con separación clara de responsabilidades
- **Manejo robusto de errores** en todos los componentes
- **Código bien documentado** con docstrings y comentarios explicativos
- **Patrones de diseño** aplicados (Repository, Factory, Strategy)
- **Testing integrado** con validación end-to-end

##  Autor

**Desarrollado como parte de prueba técnica**
-  **Autor**: Cristian Andres Sierra Paez
-  **Fecha**: Septiembre 2025
-  **Tecnologías**: Python, FastAPI, SQLAlchemy, IA/NLP
-  **Cumplimiento**: 100% de requerimientos + funcionalidades avanzadas

---

>  **Este proyecto demuestra capacidades de integración de sistemas, desarrollo de APIs, procesamiento de lenguaje natural y análisis de seguridad de manera práctica y funcional.**
