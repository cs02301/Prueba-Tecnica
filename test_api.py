#!/usr/bin/env python3
"""
Script para probar todos los endpoints de la API - ideal para capturas
"""
import requests
import json
import time

def test_api_endpoints():
    """Prueba todos los endpoints de la API y muestra resultados formateados"""
    
    base_url = "http://127.0.0.1:8003"
    
    print("="*80)
    print("🚀 PRUEBA TÉCNICA - DEMOSTRACIÓN API REST")
    print("="*80)
    print(f"📡 URL Base: {base_url}")
    print(f"📖 Documentación: {base_url}/docs")
    print()
    
    # Esperar un momento para que la API esté lista
    print("⏳ Verificando que la API esté disponible...")
    try:
        response = requests.get(f"{base_url}/items?limit=1", timeout=5)
        if response.status_code == 200:
            print("✅ API disponible y funcionando")
        else:
            print(f"❌ API respondió con código: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ No se puede conectar a la API: {e}")
        print("💡 Asegúrate de que la API esté ejecutándose con: python start_api.py")
        return
    
    print()
    
    # PRUEBA 1: Listado general
    print("📋 PRUEBA 1: LISTADO GENERAL (Límite 3)")
    print("-" * 50)
    try:
        response = requests.get(f"{base_url}/items?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total disponible: {data.get('total', 'N/A')}")
            print(f"📄 Mostrando: {len(data.get('items', []))} registros")
            print()
            for i, item in enumerate(data.get('items', [])[:3], 1):
                print(f"{i}. 📖 {item.get('title', 'N/A')}")
                print(f"   👤 Autor: {item.get('author', 'N/A')}")
                print(f"   📅 Año: {item.get('date', 'N/A')}")
                print(f"   🏷️ Género: {item.get('genre', 'N/A')}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # PRUEBA 2: Búsqueda por autor
    print("🔍 PRUEBA 2: BÚSQUEDA POR 'Garcia'")
    print("-" * 50)
    try:
        response = requests.get(f"{base_url}/items", params={"q": "Garcia"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontrados: {data.get('total', 0)} resultados")
            print()
            for i, item in enumerate(data.get('items', [])[:3], 1):
                print(f"{i}. 📖 {item.get('title', 'N/A')}")
                print(f"   👤 Autor: {item.get('author', 'N/A')}")
                print(f"   📅 Año: {item.get('date', 'N/A')}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # PRUEBA 3: Filtro por género
    print("🎭 PRUEBA 3: FILTRO POR GÉNERO 'fiction'")
    print("-" * 50)
    try:
        response = requests.get(f"{base_url}/items", params={"genre": "fiction", "limit": 3})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Libros de ficción encontrados: {data.get('total', 0)}")
            print()
            for i, item in enumerate(data.get('items', []), 1):
                print(f"{i}. 📖 {item.get('title', 'N/A')}")
                print(f"   👤 Autor: {item.get('author', 'N/A')}")
                print(f"   🏷️ Género: {item.get('genre', 'N/A')}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # PRUEBA 4: Géneros disponibles
    print("🏷️ PRUEBA 4: GÉNEROS DISPONIBLES")
    print("-" * 50)
    try:
        response = requests.get(f"{base_url}/genres")
        if response.status_code == 200:
            genres = response.json()
            print(f"✅ Total géneros únicos: {len(genres)}")
            print()
            print("Top 10 géneros más frecuentes:")
            for i, genre in enumerate(genres[:10], 1):
                print(f"{i:2d}. {genre.get('name', 'N/A')}: {genre.get('count', 0)} libro(s)")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # PRUEBA 5: Item específico
    print("📖 PRUEBA 5: CONSULTA POR ID ESPECÍFICO")
    print("-" * 50)
    try:
        # Primero obtenemos un ID válido
        response = requests.get(f"{base_url}/items?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                item_id = data['items'][0]['id']
                print(f"🔍 Consultando ID: {item_id}")
                
                # Ahora consultamos ese ID específico
                response = requests.get(f"{base_url}/items/{item_id}")
                if response.status_code == 200:
                    item = response.json()
                    print("✅ Detalles completos:")
                    print(f"   🆔 ID: {item.get('id', 'N/A')}")
                    print(f"   📖 Título: {item.get('title', 'N/A')}")
                    print(f"   👤 Autor: {item.get('author', 'N/A')}")
                    print(f"   📅 Año: {item.get('date', 'N/A')}")
                    print(f"   🏷️ Género: {item.get('genre', 'N/A')}")
                    print(f"   📂 Tipo: {item.get('type', 'N/A')}")
                    print(f"   📍 Ubicación: {item.get('location', 'N/A')}")
                    print(f"   🔗 Fuente: {item.get('source_url', 'N/A')}")
                else:
                    print(f"❌ Error consultando item: {response.status_code}")
            else:
                print("❌ No hay items disponibles para consultar")
        else:
            print(f"❌ Error obteniendo items: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("="*80)
    print("✅ PRUEBAS DE API COMPLETADAS")
    print("💡 Capturas listas para incluir en el PDF")
    print("="*80)

if __name__ == "__main__":
    test_api_endpoints()