#!/usr/bin/env python3
"""
Script para mostrar los datos de la base de datos - ideal para capturas de pantalla
"""
import sqlite3
import json

def show_database_content():
    """Muestra el contenido de la base de datos de forma organizada"""
    
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        print("="*80)
        print("📊 PRUEBA TÉCNICA - CONTENIDO DE LA BASE DE DATOS")
        print("="*80)
        print()
        
        # 1. Estadísticas generales
        total = cursor.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        print(f"📈 ESTADÍSTICAS GENERALES:")
        print(f"   • Total de registros cargados: {total}")
        print()
        
        # 2. Verificar campos disponibles
        cursor.execute("PRAGMA table_info(items)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 CAMPOS DISPONIBLES: {', '.join(columns)}")
        print()
        
        # 3. Mostrar primeros 8 registros
        print("📚 PRIMEROS 8 REGISTROS EN LA BASE DE DATOS:")
        print("-"*80)
        
        cursor.execute("""
            SELECT id, title, author, date, genre, type, location
            FROM items 
            ORDER BY title 
            LIMIT 8
        """)
        
        for i, row in enumerate(cursor.fetchall(), 1):
            id_val, title, author, date, genre, type_val, location = row
            
            # Formatear ID para mostrar solo la parte final
            id_short = id_val.split('/')[-1] if id_val else "N/A"
            
            print(f"{i:2d}. 🆔 ID: {id_short}")
            print(f"    📖 Título: {title or 'N/A'}")
            print(f"    👤 Autor: {author or 'N/A'}")
            print(f"    📅 Año: {date or 'N/A'}")
            print(f"    🏷️ Género: {genre or 'N/A'}")
            print(f"    📂 Tipo: {type_val or 'N/A'}")
            print(f"    📍 Ubicación: {location or 'N/A'}")
            print()
        
        # 4. Géneros más frecuentes
        print("🎭 GÉNEROS MÁS FRECUENTES:")
        print("-"*50)
        
        cursor.execute("""
            SELECT genre, COUNT(*) as count 
            FROM items 
            WHERE genre IS NOT NULL AND genre != '' AND genre != 'N/A'
            GROUP BY genre 
            ORDER BY count DESC 
            LIMIT 10
        """)
        
        genres = cursor.fetchall()
        if genres:
            for genre, count in genres:
                print(f"   • {genre}: {count} libro(s)")
        else:
            print("   • No hay géneros específicos cargados")
        
        print()
        
        # 5. Autores más frecuentes
        print("✍️ AUTORES MÁS FRECUENTES:")
        print("-"*50)
        
        cursor.execute("""
            SELECT author, COUNT(*) as count 
            FROM items 
            WHERE author IS NOT NULL AND author != '' AND author != 'N/A'
            GROUP BY author 
            ORDER BY count DESC 
            LIMIT 8
        """)
        
        authors = cursor.fetchall()
        if authors:
            for author, count in authors:
                print(f"   • {author}: {count} obra(s)")
        else:
            print("   • No hay autores específicos cargados")
        
        print()
        print("="*80)
        print("✅ DATOS LISTOS PARA DEMOSTRACIÓN DE LA API Y AGENTE")
        print("="*80)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al acceder a la base de datos: {e}")
        print("💡 Asegúrate de haber ejecutado: python -m etl.load")

if __name__ == "__main__":
    show_database_content()