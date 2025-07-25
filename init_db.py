#!/usr/bin/env python3
"""
Script para inicializar la base de datos en Render
"""
import os
from app import init_db, get_db_connection

def main():
    """Inicializar la base de datos"""
    try:
        print("Inicializando base de datos...")
        init_db()
        print("Base de datos inicializada correctamente")
        
        # Verificar conexión
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM inventario")
        count = cursor.fetchone()[0]
        print(f"Registros en inventario: {count}")
        conn.close()
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 