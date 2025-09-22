import os
import requests
import re
from typing import Dict, Any, Optional

# Reutilizar modelo y estructura de respuesta de la API

def run_api_request(intent: str, params: Dict[str, Any], api_base: Optional[str] = None) -> Any:
    base = api_base or os.getenv("API_BASE_URL", "http://localhost:8000")
    try:
        if intent == "detail" and params.get("id"):
            url = f"{base}/items/{params['id']}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        # Listar o buscar
        if intent in {"list", "search"}:
            url = f"{base}/items"
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        if intent == "refresh":
            url = f"{base}/admin/refresh"
            api_key = os.getenv("API_KEY", "dev-key")
            r = requests.post(url, headers={"X-API-KEY": api_key}, timeout=10)
            r.raise_for_status()
            return r.json()
        return {"error": "Invalid intent"}
    except requests.RequestException as exc:
        return {"error": str(exc)}


def format_response(data: Any, limit: int = 5) -> str:
    if isinstance(data, dict) and data.get("error"):
        return f"Lo siento, ocurrió un error: {data['error']}"
    if isinstance(data, dict) and data.get("id"):
        return f"🔎 {data.get('title')} — {data.get('author','')} ({data.get('date','')})\n{data.get('summary','')}\n{data.get('source_url','')}"
    if isinstance(data, list):
        lines = []
        for item in data[:limit]:
            lines.append(f"• {item.get('title')} — {item.get('author','')} [{item.get('date','')}]")
        return f"Top {limit} resultados:\n" + "\n".join(lines)
    return "No se encontraron resultados."


def interpret(user_text: str) -> Dict[str, Any]:
    text = user_text.strip()
    # Extraer límite
    m_lim = re.match(r"^(\d+)", text)
    limit = int(m_lim.group(1)) if m_lim else 5
    if m_lim:
        text = text[m_lim.end():].strip()
    # Extraer término de búsqueda tras 'sobre'
    m_q = re.search(r"sobre\s+(.+)", text, re.IGNORECASE)
    if m_q:
        q = m_q.group(1).strip()
        intent = "search"
    else:
        q = text
        intent = "list" if not text else "search"
    params = {"limit": limit}
    if q:
        params["q"] = q
    return {"intent": intent, "params": params, "ask": None}


def chat(user_text: str, api_base: Optional[str] = None) -> str:
    interp = interpret(user_text)
    intent = interp['intent']
    params = interp['params']
    data = run_api_request(intent, params, api_base)
    limit = params.get('limit', 5)
    if intent == 'search' and isinstance(data, list) and not data:
        fallback = run_api_request('list', {'limit': limit}, api_base)
        return f"No se encontraron coincidencias. Mostrando top {limit} resultados:\n" + format_response(fallback, limit)
    return format_response(data, limit)


if __name__ == '__main__':
    import sys
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else '5 libros'
    print(chat(query))