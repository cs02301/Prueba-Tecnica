"""
Agente de IA conversacional simplificado para la prueba técnica.

Este agente usa patrones regex para interpretar consultas en español
sin depender de servicios externos de IA, garantizando funcionalidad robusta.
"""

import re
import json
import requests
from typing import Dict, Any, Optional


class Agent:
    """
    Agente conversacional que interpreta consultas en lenguaje natural
    y las convierte en llamadas a la API REST.
    """
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8001"):
        """
        Inicializa el agente con la URL base de la API.
        
        Args:
            api_base_url: URL base de la API REST
        """
        self.api_base_url = api_base_url.rstrip('/')
    
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
        
        refresh_patterns = [
            r'actualiz(?:a|ar)',
            r'refresh',
            r'recargar?',
            r'nuevos?\s+datos?',
        ]
        
        # Detectar intención principal
        intent = "list"
        params = {}
        
        # Buscar patrones de búsqueda
        for pattern in search_patterns:
            match = re.search(pattern, query)
            if match:
                intent = "search"
                search_term = match.group(1).strip()
                
                # Extraer parámetros específicos del término de búsqueda
                params = self._extract_search_params(search_term)
                break
        
        # Buscar patrones de detalle
        if intent != "search":
            for pattern in detail_patterns:
                match = re.search(pattern, query)
                if match:
                    intent = "detail"
                    # En una implementación real, aquí extraeríamos el ID
                    params["q"] = match.group(1).strip()
                    break
        
        # Buscar patrones de actualización
        for pattern in refresh_patterns:
            if re.search(pattern, query):
                intent = "refresh"
                params = {}
                break
        
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
        
        # El resto como término general de búsqueda
        search_term = re.sub(r'\s+', ' ', search_term).strip()
        if search_term and not any(word in search_term for word in ['del', 'de', 'la', 'el', 'en', 'los', 'las']):
            params["q"] = search_term
        
        return params
    
    def call_api(self, intent: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza llamadas a la API basadas en la intención y parámetros.
        
        Args:
            intent: Intención detectada (list, search, detail, refresh)
            params: Parámetros para la llamada
            
        Returns:
            Respuesta de la API
        """
        try:
            if intent == "refresh":
                # Llamada al endpoint de actualización (requeriría autenticación en producción)
                url = f"{self.api_base_url}/admin/refresh"
                response = requests.post(url, headers={"X-API-Key": "mi-clave-secreta"})
                
            elif intent == "detail" and "id" in params:
                # Consulta por ID específico
                url = f"{self.api_base_url}/items/{params['id']}"
                response = requests.get(url)
                
            else:
                # Búsqueda general o listado
                url = f"{self.api_base_url}/items"
                query_params = {}
                
                if "q" in params:
                    query_params["search"] = params["q"]
                if "author" in params:
                    query_params["search"] = params["author"]
                if "date" in params:
                    # Buscar por año específico
                    query_params["search"] = params["date"]
                
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
            return f"""📚 **{data['title']}**
👤 Autor: {data['author']}
📅 Fecha: {data['date'] or 'No especificada'}
🔗 Más info: {data['source_url']}"""
        
        # Si es una lista de elementos
        if isinstance(data, list):
            if not data:
                return "🔍 No se encontraron resultados para tu consulta. Intenta con términos diferentes."
            
            response = f"📚 Encontré {len(data)} resultado(s) para tu consulta:\n\n"
            
            for i, item in enumerate(data, 1):
                response += f"{i}. **{item['title']}** ({item['date'] or 'Sin fecha'})\n"
                response += f"   👤 {item['author']}\n"
                if item.get('summary'):
                    response += f"   📝 {item['summary'][:100]}...\n"
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
        
        # 2. Llamar a la API
        api_result = self.call_api(interpretation["intent"], interpretation["params"])
        
        # 3. Formatear la respuesta
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