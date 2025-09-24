"""
Agente de IA conversacional simplificado para la prueba técnica.

Este agente usa patrones regex para interpretar consultas en español
sin depender de servicios externos de IA, garantizando funcionalidad robusta.
"""

import re
import difflib
import unicodedata
import json
import requests
from typing import Dict, Any, Optional


class Agent:
    """
    Agente conversacional que interpreta consultas en lenguaje natural
    y las convierte en llamadas a la API REST.
    """
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8002"):
        """
        Inicializa el agente con la URL base de la API.
        
        Args:
            api_base_url: URL base de la API REST
        """
        self.api_base_url = api_base_url.rstrip('/')
        self._last_genre_suggestions: list[str] = []
        self._last_genre_wanted: str | None = None
    
    def interpret(self, query: str) -> Dict[str, Any]:
        """
        Interpreta una consulta en lenguaje natural y extrae la intención y parámetros.
        
        Args:
            query: Consulta del usuario en español
            
        Returns:
            Diccionario con la intención y parámetros extraídos
        """
        query = query.lower().strip()
        
        # Patrones para detectar diferentes intenciones
        search_patterns = [
            r'busca(?:r)?\s+(.+)',
            r'encuentra(?:r)?\s+(.+)', 
            r'muestra(?:r)?\s+(.+)',
            r'dame\s+(.+)',
            r'quiero\s+(.+)',
            r'información\s+(?:sobre|de)\s+(.+)',
            r'¿?qué\s+(.+)\s+hay',
            r'libros?\s+(?:sobre|de)\s+(.+)',
            r'obras?\s+(?:sobre|de)\s+(.+)',
        ]
        
        detail_patterns = [
            r'detalles?\s+(?:sobre|de)\s+(.+)',
            r'más\s+información\s+(?:sobre|de)\s+(.+)',
            r'el\s+(?:libro|obra)\s+(.+)',
        ]
        
        # Patrones para detectar títulos específicos (consultas que parecen títulos de libros)
        title_patterns = [
            r'^[A-Z][a-záéíóúñü\s]+(?:en|de|del|la|el|los|las)\s+[a-záéíóúñü\s]+$',  # Títulos con artículos
            r'^[A-Z][a-záéíóúñü\s,]+$',  # Títulos generales que empiecen con mayúscula
        ]
        
        refresh_patterns = [
            r'actualiz(?:a|ar)',
            r'refresh',
            r'recargar?',
            r'nuevos?\s+datos?',
        ]
        genres_patterns = [
            r'qu[eé]\s+g[eé]neros?\s+hay',
            r'qu[eé]\s+g[eé]nero\s+hay',
            r'lista\s+de\s+g[eé]neros?',
            r'g[eé]neros?\s+disponibles',
            r'mostrar\s+g[eé]neros?',
            r'ver\s+g[eé]neros?',
            r'^g[eé]neros?$',
        ]
        
        # Detectar intención principal
        intent = "list"
        params = {}
        
        # Consultar lista de géneros (prioridad alta)
        for pattern in genres_patterns:
            if re.search(pattern, query):
                intent = "genres"
                params = {}
                break
        
        # Buscar patrones de actualización
        if intent == "list":
            for pattern in refresh_patterns:
                if re.search(pattern, query):
                    intent = "refresh"
                    params = {}
                    break

        # Buscar patrones de detalle
        if intent == "list":
            for pattern in detail_patterns:
                match = re.search(pattern, query)
                if match:
                    intent = "detail"
                    # En una implementación real, aquí extraeríamos el ID
                    params["q"] = match.group(1).strip()
                    break
        
        # Buscar patrones de búsqueda
        if intent == "list":
            for pattern in search_patterns:
                match = re.search(pattern, query)
                if match:
                    intent = "search"
                    search_term = match.group(1).strip()
                    
                    # Extraer parámetros específicos del término de búsqueda
                    params = self._extract_search_params(search_term)
                    # Mejora: extraer un año directamente del query completo si no se detectó en el término
                    if "date" not in params:
                        y = re.search(r"\b(19|20)\d{2}\b", query)
                        if y:
                            params["date"] = y.group(0)
                    break
        
        # Si no se detectó nada pero el usuario escribió algo, tratarlo como búsqueda
        if intent == "list" and query:
            intent = "search"
            params = self._extract_search_params(query)

        return {
            "intent": intent,
            "params": params
        }
    
    def _extract_search_params(self, search_term: str) -> Dict[str, Any]:
        """
        Extrae parámetros específicos de un término de búsqueda.
        
        Args:
            search_term: Término de búsqueda a analizar
            
        Returns:
            Diccionario con los parámetros extraídos
        """
        params = {}
        
        # Detectar autores conocidos
        authors = [
            "garcía márquez", "gabriel garcía márquez",
            "pablo picasso", "picasso",
            "karl marx", "marx",
            "cervantes", "shakespeare",
            "borges", "cortázar"
        ]
        
        for author in authors:
            if author in search_term.lower():
                params["author"] = author.title()
                # Remover el autor del término de búsqueda general
                search_term = re.sub(r'\b' + re.escape(author) + r'\b', '', search_term, flags=re.IGNORECASE)
                break
        
        # Detectar años
        year_match = re.search(r'\b(19|20)\d{2}\b', search_term)
        if year_match:
            params["date"] = year_match.group(0)
            search_term = re.sub(r'\b(19|20)\d{2}\b', '', search_term)
        
        # Detectar tipos
        if re.search(r'\b(?:libros?|book)\b', search_term):
            params["type"] = "book"
            search_term = re.sub(r'\b(?:libros?|book)\b', '', search_term)

        # Detectar género aproximado por palabras clave comunes
        # p.ej., terror, ciencia ficción, romance, crimen, historia, arte
        genre_map = {
            "terror": "horror",
            "ciencia ficcion": "science fiction",
            "ciencia ficción": "science fiction",
            "romance": "romance",
            "crimen": "crime",
            "policiaca": "crime",
            "historia": "history",
            "arte": "art",
            "fantasia": "fantasy",
            "fantasía": "fantasy",
            "misterio": "mystery",
            "biografia": "biography",
            "biografía": "biography",
            "fisica": "physics",
            "física": "physics",
        }
        normalized = (
            search_term.lower()
            .replace("ficción", "ficcion")
            .replace("fantasía", "fantasia")
            .replace("biografía", "biografia")
        )
        for kw, en in genre_map.items():
            if kw in normalized:
                params["genre"] = en
                # eliminar la palabra clave del término general
                search_term = re.sub(re.escape(kw), '', normalized, flags=re.IGNORECASE)
                break
        
        # El resto como término general de búsqueda
        search_term = re.sub(r'\s+', ' ', search_term).strip()
        if search_term:
            # Si no hay otros parámetros específicos, usar el término completo
            if not any(key in params for key in ['author', 'genre', 'type']):
                params["q"] = search_term
            elif search_term and not any(word in search_term for word in ['del', 'de', 'la', 'el', 'en', 'los', 'las']):
                params["q"] = search_term
        
        return params

    # --- Utilidades de géneros ---
    @staticmethod
    def _normalize(text: str) -> str:
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        return text.lower().strip()

    def _fetch_genres(self) -> list[str]:
        try:
            r = requests.get(f"{self.api_base_url}/genres", timeout=10)
            if r.status_code == 200:
                data = r.json()
                return [g.get('name', '') for g in data if isinstance(g, dict)]
        except requests.RequestException:
            pass
        return []

    def _resolve_genre(self, wanted: str) -> str | None:
        """
        Trata de mapear el género solicitado a uno disponible vía /genres.
        Usa normalización y fuzzy matching. Devuelve el nombre original tal como aparece en /genres.
        """
        self._last_genre_suggestions = []
        self._last_genre_wanted = wanted
        genres = self._fetch_genres()
        if not genres:
            return None
        norm_w = self._normalize(wanted)
        # Coincidencia por inclusión directa
        for g in genres:
            if norm_w in self._normalize(g) or self._normalize(g) in norm_w:
                return g
        # Fuzzy matching
        matches = difflib.get_close_matches(norm_w, [self._normalize(g) for g in genres], n=5, cutoff=0.6)
        if matches:
            # devolver el primero en forma original
            target_norm = matches[0]
            for g in genres:
                if self._normalize(g) == target_norm:
                    return g
        # preparar sugerencias para el usuario
        self._last_genre_suggestions = genres[:10]
        return None
    
    def call_api(self, intent: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza llamadas a la API basadas en la intención y parámetros.
        
        Args:
            intent: Intención detectada (list, search, detail, refresh, genres)
            params: Parámetros para la llamada
            
        Returns:
            Respuesta de la API
        """
        try:
            if intent == "refresh":
                # Llamada al endpoint de actualización (requeriría autenticación en producción)
                url = f"{self.api_base_url}/admin/refresh"
                response = requests.post(url, headers={"X-API-Key": "mi-clave-secreta"})
            elif intent == "genres":
                url = f"{self.api_base_url}/genres"
                response = requests.get(url)
                
            elif intent == "detail" and "id" in params:
                # Consulta por ID específico
                url = f"{self.api_base_url}/items/{params['id']}"
                response = requests.get(url)
                
            else:
                # Búsqueda general o listado
                url = f"{self.api_base_url}/items"
                query_params: Dict[str, Any] = {}

                # El endpoint espera 'q' para búsqueda de texto en título/ubicación,
                # 'author' para filtrar por autor y 'type' para categoría.
                q_value: Optional[str] = None
                if "q" in params and params["q"]:
                    q_value = params["q"]
                # Si se detectó un año, úsalo como parte de la búsqueda general
                if "date" in params and params["date"]:
                    q_value = f"{q_value} {params['date']}".strip() if q_value else params["date"]
                if q_value:
                    query_params["q"] = q_value

                if "author" in params and params["author"]:
                    query_params["author"] = params["author"]
                if "type" in params and params["type"]:
                    query_params["type"] = params["type"]
                if "genre" in params and params["genre"]:
                    resolved = self._resolve_genre(params["genre"])
                    if resolved:
                        # priorizar filtro por género
                        query_params.pop("q", None)
                        query_params["genre"] = resolved
                elif "q" in params and params["q"]:
                    # Si no venía género pero 'q' podría ser un género, intentar resolverlo
                    resolved = self._resolve_genre(params["q"])
                    if resolved:
                        query_params.pop("q", None)
                        query_params["genre"] = resolved

                # Limitar resultados para mejor experiencia
                query_params["limit"] = 5

                response = requests.get(url, params=query_params)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
                
        except requests.RequestException as e:
            return {"success": False, "error": f"Error de conexión: {str(e)}"}
    
    def format_response(self, api_result: Dict[str, Any], original_query: str) -> str:
        """
        Formatea la respuesta de la API en lenguaje natural.
        
        Args:
            api_result: Resultado de la llamada a la API
            original_query: Consulta original del usuario
            
        Returns:
            Respuesta formateada para el usuario
        """
        if not api_result["success"]:
            return f"❌ Lo siento, hubo un problema: {api_result['error']}"
        
        data = api_result["data"]
        
        # Si es un solo elemento (consulta por ID)
        if isinstance(data, dict) and "id" in data:
            response = f"""📚 **{data['title']}**
🆔 ID: {data.get('id', 'N/A')}
� Fecha: {data.get('date') or 'No especificada'}
�👤 Autor: {data.get('author') or 'No especificado'}"""
            if data.get('location'):
                response += f"\n📍 Ubicación: {data['location']}"
            if data.get('type'):
                response += f"\n📂 Tipo: {data['type']}"
            if data.get('genre'):
                response += f"\n🏷️ Género: {data['genre']}"
            if data.get('summary'):
                response += f"\n📝 Resumen: {data['summary']}"
            if data.get('source_url'):
                response += f"\n🔗 Fuente: {data['source_url']}"
            return response
        
        # Lista de géneros
        if isinstance(data, list) and data and isinstance(data[0], dict) and 'name' in data[0] and 'count' in data[0]:
            lines = [f"• {g['name']} ({g['count']})" for g in data[:20]]
            return "📚 Géneros disponibles:\n" + "\n".join(lines)

        # Si es una lista de elementos
        if isinstance(data, list):
            if not data:
                msg = "🔍 No se encontraron resultados para tu consulta. Intenta con términos diferentes."
                if self._last_genre_wanted and self._last_genre_suggestions:
                    sug = ", ".join(self._last_genre_suggestions[:5])
                    msg += f"\n💡 No encontré el género '{self._last_genre_wanted}'. Prueba con alguno de estos: {sug}."
                return msg
            
            response = f"📚 Encontré {len(data)} resultado(s) para tu consulta:\n\n"
            
            for i, item in enumerate(data, 1):
                response += f"{i}. **{item['title']}** ({item['date'] or 'Sin fecha'})\n"
                response += f"   🆔 ID: {item.get('id', 'N/A')}\n"
                response += f"   👤 Autor: {item.get('author') or 'No especificado'}\n"
                if item.get('location'):
                    response += f"   📍 Ubicación: {item['location']}\n"
                if item.get('type'):
                    response += f"   📂 Tipo: {item['type']}\n"
                if item.get('genre'):
                    response += f"   🏷️ Género: {item['genre']}\n"
                if item.get('summary'):
                    response += f"   📝 Resumen: {item['summary'][:150]}{'...' if len(item['summary']) > 150 else ''}\n"
                if item.get('source_url'):
                    response += f"   🔗 Fuente: {item['source_url']}\n"
                response += "\n"
            
            if len(data) == 5:
                response += "💡 Puedes hacer consultas más específicas para obtener mejores resultados."
            
            return response
        
        return "✅ Operación completada exitosamente."
    
    def chat(self, query: str) -> str:
        """
        Procesa una consulta completa del usuario y devuelve una respuesta.
        
        Args:
            query: Consulta del usuario en lenguaje natural
            
        Returns:
            Respuesta procesada y formateada
        """
        # 1. Interpretar la consulta
        interpretation = self.interpret(query)
        
        # 2. Si parece búsqueda directa por título, usar la consulta original
        if (interpretation["intent"] == "search" and 
            len(query.strip().split()) > 2 and 
            query[0].isupper() and
            "q" in interpretation["params"]):
            interpretation["params"]["q"] = query.strip()
        
        # 3. Llamar a la API
        api_result = self.call_api(interpretation["intent"], interpretation["params"])
        
        # 4. Formatear la respuesta
        return self.format_response(api_result, query)





def main():
    """Función principal para probar el agente interactivamente."""
    print("🤖 Agente de IA iniciado. Escribe 'salir' para terminar.")
    print("💡 Ejemplos de consultas:")
    print("   - Busca libros de García Márquez")
    print("   - ¿Qué libros hay del año 1985?")
    print("   - Muéstrame información sobre Pablo Picasso")
    print()
    
    agent = Agent()
    
    while True:
        query = input("👤 Tú: ").strip()
        
        if query.lower() in ['salir', 'exit', 'quit', 'adiós']:
            print("🤖 ¡Hasta luego!")
            break
        
        if not query:
            continue
        
        try:
            response = agent.chat(query)
            print(f"🤖 Agente: {response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()