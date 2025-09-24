# 🚀 Guía de Uso Rápido

## Introducción
Este sistema permite buscar libros y documentos usando **lenguaje natural en español**. El agente IA entiende tus consultas y te ayuda a encontrar exactamente lo que buscas.

## ⚡ Inicio Rápido (30 segundos)

### 1. Instalar y Ejecutar
```bash
# Clonar y configurar
git clone https://github.com/cs02301/Prueba-Tecnica.git
cd Prueba-Tecnica
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Ejecutar sistema completo
python test_system.py
```

### 2. Usar el Agente Interactivo
```bash
python agent/agent_simple.py
```

### 3. Probar la API Directamente
Visita: http://127.0.0.1:8002/docs

## 💬 Ejemplos de Consultas

### Búsquedas Básicas
- `"García Márquez"` → Encuentra libros del autor
- `"libros de 1985"` → Libros publicados en ese año
- `"Pablo Picasso"` → Información sobre Picasso

### 🆕 Búsquedas por Género
- `"qué géneros hay"` → Lista todos los géneros disponibles
- `"libros de ficción"` → Libros del género ficción
- `"ciencia ficción"` → Libros de ciencia ficción
- `"biografías"` → Libros biográficos
- `"novelas"` → Novelas disponibles

### Búsquedas Específicas
- `"El amor en los tiempos del cólera"` → Libro específico
- `"Crónica de una muerte anunciada"` → Otro libro específico
- `"amor"` → Búsqueda general por tema

## 📋 Respuestas del Sistema

### Formato de Respuesta Completo
```
📚 Encontré 2 resultado(s) para tu consulta:

1. **El amor en los tiempos del cólera** (1985)
   🆔 ID: works/OL274518W
   👤 Autor: Gabriel García Márquez
   📍 Ubicación: No especificada
   📂 Tipo: book
   🏷️ Género: Vida familiar, Love stories, Ficció històrica
   📝 Resumen: Una épica historia de amor...
   🔗 Fuente: https://openlibrary.org/works/OL274518W

2. **Crónica de una muerte anunciada** (1980)
   🆔 ID: works/OL274574W
   👤 Autor: Gabriel García Márquez
   📂 Tipo: book
   🏷️ Género: Death, Spanish language books
   🔗 Fuente: https://openlibrary.org/works/OL274574W
```

### Lista de Géneros
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
```

## 🛠️ Uso Programático

### Integrar en tu Código
```python
from agent.agent_simple import Agent

# Crear agente
agent = Agent("http://127.0.0.1:8002")

# Hacer consultas
resultado = agent.chat("libros de García Márquez")
print(resultado)

# Consultar géneros
generos = agent.chat("qué géneros hay")
print(generos)

# Buscar por género específico
ficcion = agent.chat("libros de ficción")
print(ficcion)
```

### Usar la API Directamente
```python
import requests

# Listar items
response = requests.get("http://127.0.0.1:8002/items?limit=5")
items = response.json()

# Buscar por género
response = requests.get("http://127.0.0.1:8002/items?genre=fiction")
fiction_books = response.json()

# Obtener géneros disponibles
response = requests.get("http://127.0.0.1:8002/genres")
genres = response.json()
```

## 🔧 Configuración Avanzada

### Variables de Entorno Opcionales
```bash
# Personalizar query de Open Library
export OPENLIBRARY_QUERY="gabriel garcia marquez"

# Cambiar API key administrativa
export API_KEY="mi-clave-super-secreta"

# Puerto personalizado
export API_PORT=8001
```

### Comandos de Verificación
```bash
# Verificar base de datos
python -c "import sqlite3; db=sqlite3.connect('data.db'); print('Registros:', db.execute('SELECT COUNT(*) FROM items').fetchone()[0])"

# Probar API
curl "http://127.0.0.1:8002/items?limit=3"

# Probar géneros
curl "http://127.0.0.1:8002/genres"
```

## ❓ Preguntas Frecuentes

### ¿Por qué no encuentra un género?
El sistema usa **fuzzy matching**. Si escribes "ficcion" sin tilde, encontrará "fiction". Si no encuentra el género exacto, te sugerirá alternativas.

### ¿Cómo actualizar los datos?
```bash
# Método 1: Re-ejecutar ETL
python -c "from etl.load import run; run()"

# Método 2: API administrativa
curl -X POST "http://127.0.0.1:8002/admin/refresh" -H "X-API-Key: mi-clave-secreta"
```

### ¿Qué hacer si no hay resultados?
- Intenta términos más generales
- Revisa la ortografía
- Usa sinónimos (ej: "novel" en lugar de "novela")
- El sistema te dará sugerencias automáticamente

### ¿Puedo agregar más fuentes de datos?
Sí, modifica `etl/load.py` para agregar más APIs o fuentes de datos.

## 🆕 Funcionalidades Destacadas

### ✨ Nuevas en Versión 2.0
- **Géneros inteligentes**: El sistema reconoce géneros en español e inglés
- **Sugerencias automáticas**: Te ayuda cuando no encuentra lo que buscas
- **Respuestas completas**: Todos los campos normalizados en formato claro
- **Fallback robusto**: Siempre hay datos disponibles, incluso si falla la API externa

### 🎯 Capacidades del Agente
- Interpreta **lenguaje natural** en español
- **Mapea géneros** automáticamente (ficción → fiction)
- **Resuelve ambigüedades** con fuzzy matching
- **Sugiere alternativas** cuando no encuentra resultados exactos
- **Formatea respuestas** con iconos y estructura clara

---

¿Necesitas ayuda? El sistema está diseñado para ser intuitivo. ¡Solo escribe lo que buscas en español natural! 🇪🇸