"""
Agente de IA conversacional para la prueba técnica.

El agente acepta consultas en lenguaje natural, determina la intención de la
consulta, extrae parámetros relevantes e interactúa con la API para devolver
resultados estructurados o solicitar aclaraciones. Usa la API de DeepSeek vía
la librería ``requests`` para interpretar la entrada del usuario.

Uso::

    from agent.agent import chat
    response = chat("Muestra libros sobre Colombia después de 1980")
    print(response)

Para ejecutar el agente como CLI, ejecuta este archivo directamente::

    python -m agent.agent
"""
from __future__ import annotations

import os
import json
import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyCbXuzgAD8dwujOiimQ1veG4eVs4DPwVjI")

SCHEMA_PROMPT = """\
Eres un asistente que transforma preguntas de un usuario en intenciones estructuradas \
para una API REST. Responde únicamente con JSON que tenga la siguiente estructura:
{
  "intent": "list" | "search" | "detail" | "refresh" | "clarify",
  "params": {
    "q": string opcional,
    "author": string opcional,
    "type": string opcional,
    "location": string opcional,
    "id": string opcional
  },
  "ask": string opcional
}
El campo ``intent`` describe la acción: ``list`` para listar registros, ``search`` \
cuando hay términos de búsqueda o filtros, ``detail`` para solicitar un ítem por id, \
``refresh`` para solicitar la actualización de la base de datos y ``clarify`` cuando \
no hay suficiente información y necesitas pedir un dato adicional al usuario. El campo \
``params`` contiene los parámetros relevantes para la llamada a la API. El campo \
``ask`` solo debe rellenarse si ``intent`` es ``clarify`` y debe incluir una pregunta \
que ayude a completar la información faltante.

Ejemplos:

Usuario: "Muéstrame 10 libros sobre Medellín escritos por García después de 2000"
JSON esperado: {
  "intent": "search",
  "params": {
    "q": "libros Medellín",
    "author": "García",
    "type": "book"
  },
  "ask": ""
}

Usuario: "Actualiza los datos"
JSON esperado: {
  "intent": "refresh",
  "params": {},
  "ask": ""
}
"""

BASE_URL = "https://api.deepseek.com"
API_KEY = "sk-48b44b40656f4481806c38fa82803745"

class ItemOut(BaseModel):
    id: str
    title: str
    date: Optional[str] = None
    author: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    summary: Optional[str] = None
    source_url: Optional[str] = None

    class Config:
        from_attributes = True

def interpret(user_text: str) -> Dict[str, Any]:
    """
    Call the Gemini API to interpret the user's natural language query.
    Returns a dict with keys intent, params, ask
    """
    prompt = SCHEMA_PROMPT + "\n" + user_text
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    text = response.text
    # Remove markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # remove first fence line
        if lines[0].startswith("```"):
            lines = lines[1:]
        # remove last fence line
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    try:
        result = json.loads(text)
        # Post-process params for common patterns
        params = result.get("params", {})
        # Extract a leading number as limit and strip it from the query
        import re
        text_str = user_text.strip()
        m = re.match(r"^(\d+)\s+(.*)$", text_str)
        if m:
            params["limit"] = int(m.group(1))
            text_str = m.group(2)
        # Fallback: use cleaned text as query if missing
        if not params.get("q"):
            params["q"] = text_str
        # Default type to 'book' if missing or empty
        if not params.get("type"):
            params["type"] = "book"
        return {
            "intent": result.get("intent"),
            "params": params,
            "ask": result.get("ask"),
        }
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse JSON from Gemini: {text}") from exc

def run_api_request(intent: str, params: Dict[str, Any], api_base: Optional[str] = None) -> Any:
    """
    Execute the appropriate API call based on the interpreted intent.

    Parameters
    ----------
    intent : str
        One of ``list``, ``search``, ``detail`` or ``refresh``.
    params : dict
        Parameters extracted by the ``interpret`` function.
    api_base : str, optional
        Base URL of the API. Defaults to ``http://localhost:8000``.

    Returns
    -------
    Any
        Parsed JSON response from the API or error information.
    """
    base = api_base or os.getenv("API_BASE_URL", "http://localhost:8000")
    try:
        if intent == "detail" and params.get("id"):
            item_id = params["id"]
            url = f"{base}/items/{item_id}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        elif intent in {"list", "search"}:
            url = f"{base}/items"
            # Remove None values
            query_params = {k: v for k, v in params.items() if v}
            r = requests.get(url, params=query_params, timeout=10)
            r.raise_for_status()
            return r.json()
        elif intent == "refresh":
            api_key = os.getenv("API_KEY", "dev-key")
            url = f"{base}/admin/refresh"
            r = requests.post(url, headers={"X-API-KEY": api_key}, timeout=10)
            r.raise_for_status()
            return r.json()
        else:
            return {"error": "clarify"}
    except requests.ConnectionError:
        return {"error": "Parece que la API no se está ejecutando en http://localhost:8000. Inicia el servidor con 'uvicorn api.main:app --reload'"}
    except requests.RequestException as exc:
        return {"error": f"API request failed: {exc}"}

def format_response(data: Any, limit: int = 5) -> str:
    """
    Format the API response into a user-friendly message.

    Parameters
    ----------
    data : Any
        Parsed JSON returned from the API request.

    Returns
    -------
    str
        Message suitable to return to the user.

    Notes
    -----
    - For a single item, return detailed information.
    - For a list of items, return the top five with summary info.
    - If an error is present, return a helpful error message.
    """
    if isinstance(data, dict) and data.get("error"):
        return f"Lo siento, ocurrió un error: {data['error']}"
    # Single item
    if isinstance(data, dict) and data.get("id"):
        title = data.get("title", "(sin título)")
        author = data.get("author", "")
        date = data.get("date", "")
        summary = data.get("summary", "")
        url = data.get("source_url", "")
        return f"🔎 {title} — {author} ({date})\n{summary}\n{url}"
    # List of items
    if isinstance(data, list):
        lines = []
        for item in data[:limit]:
            title = item.get("title", "(sin título)")
            author = item.get("author", "")
            date = item.get("date", "")
            lines.append(f"• {title} — {author} [{date}]")
    return f"Top {limit} resultados:\n" + "\n".join(lines)
    # Fallback
    return "No se encontraron resultados."

def chat(user_text: str, api_base: Optional[str] = None) -> str:
    """
    Process a user's message end-to-end: interpret, query and format.

    Parameters
    ----------
    user_text : str
        The raw input from the user.
    api_base : str, optional
        Override the API base URL.

    Returns
    -------
    str
        Response generated by the agent.
    """
    try:
        interpretation = interpret(user_text)
    except Exception as exc:
        return f"Ocurrió un error al interpretar tu mensaje: {exc}"
    # If the model asks for clarification, return its question
    if interpretation.get("ask"):
        return interpretation["ask"]
    intent = interpretation.get("intent")
    # Fallback: treat unknown intent as list and drop filters
    if intent not in {"list", "search", "detail", "refresh"}:
        intent = "list"
        # clear query filters for generic listing
        original_limit = interpretation.get("params", {}).get("limit")
    import re

    def chat(user_text: str, api_base: Optional[str] = None) -> str:
        """
        Bypass interpretation: list top N items based on numeric prefix or default 5.
        """
        # Extract leading number for limit, default to 5
        m = re.match(r"^(\d+)", user_text.strip())
        limit = int(m.group(1)) if m else 5
        # Query the API to list items
        data = run_api_request("list", {"limit": limit}, api_base=api_base)
        return format_response(data)
    data = run_api_request(intent, params, api_base=api_base)
    limit = params.get("limit", 5)
    # Si búsqueda no arroja resultados, fallback a listado genérico
    if intent == "search" and isinstance(data, list) and not data:
        fallback = run_api_request("list", {"limit": limit}, api_base=api_base)
        formatted = format_response(fallback, limit=limit)
        return f"No se encontraron coincidencias. Mostrando top {limit} resultados:\n" + formatted
    return format_response(data, limit=limit)