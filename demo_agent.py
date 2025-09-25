#!/usr/bin/env python3
"""
Script para demostrar el agente IA - ideal para capturas
"""
from agent.agent_simple import Agent
import time

def demo_agent():
    """Demuestra las capacidades del agente IA"""
    
    print("="*80)
    print("🤖 PRUEBA TÉCNICA - DEMOSTRACIÓN AGENTE IA")
    print("="*80)
    print("🌐 Conectando a API: http://127.0.0.1:8003")
    print()
    
    try:
        # Inicializar agente
        agent = Agent("http://127.0.0.1:8003")
        
        # Consultas de demostración
        consultas = [
            ("🏷️ CONSULTA 1: Géneros Disponibles", "qué géneros hay"),
            ("🔍 CONSULTA 2: Búsqueda por Género", "fiction"),
            ("👤 CONSULTA 3: Búsqueda por Autor", "García Márquez"),
            ("📅 CONSULTA 4: Búsqueda por Año", "libros de 1998"),
            ("📖 CONSULTA 5: Consulta Específica", "A Clash of Kings")
        ]
        
        for titulo, consulta in consultas:
            print(titulo)
            print("-" * 60)
            print(f"👤 Usuario: {consulta}")
            print()
            print("🤖 Agente IA:")
            
            try:
                respuesta = agent.chat(consulta)
                print(respuesta)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
            print("=" * 80)
            print()
            
            # Pausa breve entre consultas
            time.sleep(1)
        
        print("✅ DEMOSTRACIÓN DEL AGENTE IA COMPLETADA")
        print("💡 Capturas listas para incluir en el PDF")
        
    except Exception as e:
        print(f"❌ Error conectando con la API: {e}")
        print("💡 Asegúrate de que la API esté funcionando en puerto 8003")

if __name__ == "__main__":
    demo_agent()