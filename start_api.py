#!/usr/bin/env python3
"""
Script para iniciar la API REST para demostraciones
"""
import uvicorn
import sys
import os

# Agregar el directorio actual al path
sys.path.append('.')

# Importar la aplicación
from api.main import app

if __name__ == "__main__":
    print("🚀 Iniciando API REST para demostraciones...")
    print("📡 URL: http://127.0.0.1:8003")
    print("📖 Documentación: http://127.0.0.1:8003/docs")
    print("⏹️  Para detener: Ctrl+C")
    print()
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8003,
        log_level="info"
    )