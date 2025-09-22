# Prueba Técnica – ETL, API REST y Agente IA

Este repositorio contiene la solución base a la prueba técnica descrita en el
documento proporcionado. El proyecto se compone de tres capas principales:

1. **ETL/ELT** que obtiene datos de una fuente pública, los normaliza y los
   almacena en una base de datos relacional.
2. **API REST** construida con FastAPI que expone los datos para ser
   consultados y permite refrescar la base mediante un endpoint protegido.
3. **Agente de IA** que interpreta consultas en lenguaje natural, llama a la
   API y devuelve respuestas amigables o solicita aclaraciones si es necesario.

## Estructura del proyecto

```
.
├── etl/                  # Carga y transformación de datos
│   ├── __init__.py
│   └── load.py           # Script de ETL (ejecutable)
├── api/                  # Servidor FastAPI
│   ├── __init__.py
│   └── main.py           # Definición de rutas y modelos Pydantic
├── agent/                # Lógica del agente de IA
│   ├── __init__.py
│   └── agent.py          # CLI y funciones de interpretación
├── docs/
│   ├── security.md       # Riesgos y mitigaciones (opcional)
├── models_shared.py      # Modelos SQLAlchemy comunes
├── requirements.txt      # Dependencias de Python
├── README.md             # Este archivo
└── .env                  # Variables de entorno (no se incluye por defecto)
```

## Requisitos

* Python 3.10 o superior
* Un motor de base de datos compatible con SQLAlchemy. Por defecto se usa SQLite
  y no requiere instalación adicional.

### Instalación de dependencias

Crea un entorno virtual y instala las dependencias:

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

En Windows PowerShell usa:

```powershell
.venv\Scripts\Activate.ps1
```

En Windows CMD usa:

```cmd
.venv\Scripts\activate.bat
```

## Configuración

Las variables de entorno se pueden definir en un archivo `.env` (no incluido en
el repositorio) o exportarse en la sesión. Las variables principales son:

* `DB_URL`: URL de la base de datos para SQLAlchemy (por ejemplo,
  `sqlite:///./data.db` o `postgresql+psycopg://usuario:password@host/db`).
* `API_KEY`: Clave utilizada para proteger el endpoint `/admin/refresh`. Se
  emplea en el encabezado `X-API-KEY`.
* `OPENLIBRARY_QUERY`: Palabra clave para la búsqueda en la API de Open Library
  usada por defecto en el ETL (`colombia` si se omite).
* `OPENAI_API_KEY`: Clave para usar el modelo de OpenAI en el agente.
* `API_BASE_URL`: Base URL de la API para que el agente realice llamadas
  (por defecto `http://localhost:8000`).

## Ejecución del ETL

Para cargar los datos en la base de datos:

```bash
python -m etl.load
```

Este comando descargará registros públicos (por defecto de Open Library), los
normalizará y los insertará en la tabla `items`. Si el script se ejecuta de
nuevo, los registros se sobrescribirán o actualizarán según su ID.

## Lanzar la API

Puedes arrancar el servidor FastAPI con Uvicorn:

```bash
uvicorn api.main:app --reload
```

* `GET /items`: Lista los ítems. Admite parámetros de consulta `q`, `author`,
  `type`, `location`, `limit` y `offset`.
* `GET /items/{id}`: Devuelve el detalle de un ítem.
* `POST /admin/refresh`: Vuelve a ejecutar el ETL (requiere encabezado `X-API-KEY`).

Ejemplo de solicitud con `curl`:

```bash
# Listar con búsqueda
curl 'http://localhost:8000/items?q=historia&author=García'

# Refrescar datos
curl -X POST 'http://localhost:8000/admin/refresh' -H 'X-API-KEY: TU_API_KEY'
```

Una vez en ejecución, la documentación interactiva de la API está disponible en
`http://localhost:8000/docs`.

## Usar el agente de IA

El agente interpreta preguntas en lenguaje natural y devuelve un resumen o un
pedido de aclaración. Para usarlo desde la línea de comandos:

```bash
python -m agent.agent "Muéstrame libros sobre Bogotá publicados antes de 1990"
```

Si el modelo detecta que falta información para ejecutar la consulta (por
ejemplo, un ID para el detalle), responderá con una pregunta. Para su
funcionamiento es necesario tener una clave de OpenAI válida en
`OPENAI_API_KEY`.

## Notas adicionales

* El proyecto incluye un documento opcional (`docs/security.md`) que reflexiona
  sobre consideraciones de seguridad y privacidad.
* La carpeta `docs/screenshots.pdf` se menciona en el enunciado original para
  incluir capturas de la base de datos, la API y el agente funcionando. Puedes
  generar dicho PDF durante la entrega final según se solicite.
* El modelo del agente utiliza un esquema simple para extraer intenciones y
  parámetros. En contextos reales conviene añadir validación y gestionar
  respuestas ambiguas con mayor detalle.