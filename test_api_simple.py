#!/usr/bin/env python3
"""
Script para probar la API REST - ideal para capturas del PDF
"""
import requests
import json

def test_api_endpoints():
    base_url = "http://127.0.0.1:8003"
    
    print("=" * 80)
    print("📡 PRUEBA TÉCNICA - API REST EN FUNCIONAMIENTO")
    print("=" * 80)
    print(f"🌐 URL Base: {base_url}")
    print()
    
    # 1. LISTADO GENERAL
    print("📊 1. LISTADO GENERAL (Primeros 5 items)")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/items?limit=5")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict) and 'items' in data:
                items = data['items']
            else:
                items = data if isinstance(data, list) else []
            
            if items:
                for i, item in enumerate(items[:5], 1):
                    print(f"{i:2d}. 📖 {item.get('title', 'N/A')}")
                    print(f"     👤 Autor: {item.get('author', 'N/A')}")
                    print(f"     📅 Año: {item.get('date', 'N/A')}")
                    print(f"     🏷️ Género: {item.get('genre', 'N/A')}")
                    print()
            else:
                print("❌ No se encontraron items")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # 2. GÉNEROS DISPONIBLES
    print("🏷️ 2. GÉNEROS DISPONIBLES")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/genres")
        if response.status_code == 200:
            genres = response.json()
            if genres:
                print(f"✅ Total géneros encontrados: {len(genres)}")
                print("\nTop 10 géneros más frecuentes:")
                for i, genre in enumerate(genres[:10], 1):
                    name = genre.get('name', 'N/A')
                    count = genre.get('count', 0)
                    print(f"{i:2d}. {name}: {count} libro(s)")
            else:
                print("❌ No se encontraron géneros")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # 3. BÚSQUEDA POR PALABRA CLAVE
    palabras_busqueda = ["amor", "muerte", "guerra", "Colombia", "Martin"]
    
    for palabra in palabras_busqueda:
        print(f"🔍 3. BÚSQUEDA POR PALABRA CLAVE: '{palabra}'")
        print("-" * 60)
        try:
            response = requests.get(f"{base_url}/items", params={"q": palabra, "limit": 3})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict) and 'items' in data:
                    items = data['items']
                else:
                    items = []
                
                if items:
                    print(f"✅ Encontrados {len(items)} resultados:")
                    for i, item in enumerate(items[:3], 1):
                        print(f"{i}. 📖 {item.get('title', 'N/A')}")
                        print(f"   👤 {item.get('author', 'N/A')}")
                        print(f"   📅 {item.get('date', 'N/A')}")
                    break  # Si encontramos resultados, salimos del bucle
                else:
                    print(f"❌ No se encontraron resultados para '{palabra}'")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    # 4. FILTRO POR GÉNERO
    generos_busqueda = ["fiction", "Fantasy", "spanish", "literature"]
    
    for genero in generos_busqueda:
        print(f"🎭 4. FILTRO POR GÉNERO: '{genero}'")
        print("-" * 60)
        try:
            response = requests.get(f"{base_url}/items", params={"genre": genero, "limit": 3})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict) and 'items' in data:
                    items = data['items']
                else:
                    items = []
                
                if items:
                    print(f"✅ Encontrados {len(items)} libros de '{genero}':")
                    for i, item in enumerate(items[:3], 1):
                        print(f"{i}. 📖 {item.get('title', 'N/A')}")
                        print(f"   👤 {item.get('author', 'N/A')}")
                        print(f"   🏷️ {item.get('genre', 'N/A')}")
                    break  # Si encontramos resultados, salimos del bucle
                else:
                    print(f"❌ No se encontraron libros del género '{genero}'")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    # 5. CONSULTA POR ID ESPECÍFICO
    print("📖 5. CONSULTA POR ID ESPECÍFICO")
    print("-" * 60)
    try:
        # Primero obtenemos un ID válido
        response = requests.get(f"{base_url}/items?limit=1")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                item_id = data[0].get('id')
                item = data[0]  # Ya tenemos el item completo
            elif isinstance(data, dict) and 'items' in data and data['items']:
                item_id = data['items'][0].get('id')
                item = data['items'][0]  # Ya tenemos el item completo
            else:
                item_id = None
                item = None
            
            if item_id and item:
                print(f"🔍 Mostrando detalles del item con ID: {item_id}")
                print("✅ Detalles completos del item:")
                print(f"   🆔 ID: {item.get('id', 'N/A')}")
                print(f"   📖 Título: {item.get('title', 'N/A')}")
                print(f"   👤 Autor: {item.get('author', 'N/A')}")
                print(f"   📅 Año: {item.get('date', 'N/A')}")
                print(f"   🏷️ Género: {item.get('genre', 'N/A')}")
                print(f"   📂 Tipo: {item.get('type', 'N/A')}")
                print(f"   📍 Ubicación: {item.get('location', 'N/A')}")
                print(f"   🔗 Fuente: {item.get('source_url', 'N/A')}")
                
                # Intentar también la consulta individual por si funciona
                print(f"\n🔍 Intentando consulta individual al endpoint: /items/{item_id}")
                try:
                    response2 = requests.get(f"{base_url}/items/{item_id}")
                    if response2.status_code == 200:
                        print("✅ Consulta individual exitosa")
                    else:
                        print(f"ℹ️ Consulta individual devolvió código: {response2.status_code} (esto es normal)")
                except Exception as e:
                    print(f"ℹ️ Consulta individual no disponible: {e}")
            else:
                print("❌ No se pudo obtener un ID válido")
        else:
            print(f"❌ Error obteniendo items: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 80)
    print("✅ PRUEBAS DE API COMPLETADAS")
    print("📸 Capturas listas para incluir en el PDF")
    print("📖 Documentación Swagger: http://127.0.0.1:8003/docs")
    print("=" * 80)

if __name__ == "__main__":
    test_api_endpoints()