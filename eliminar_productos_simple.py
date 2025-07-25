#!/usr/bin/env python3
"""
Script simplificado para eliminar productos obsoletos sin pandas
"""
import os
import csv
from datetime import datetime

# Importar funciones de la aplicación principal
from app import get_db_connection, DATABASE_TYPE

def backup_antes_de_eliminar():
    """Crear backup antes de eliminar productos obsoletos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener todos los registros
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('SELECT * FROM registros')
        else:
            cursor.execute('SELECT * FROM registros')
        
        registros = cursor.fetchall()
        conn.close()
        
        # Crear backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_antes_eliminar_{timestamp}.csv"
        
        with open(backup_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'medicamento', 'cantidad', 'precio', 'fecha', 'fecha_ingreso', 
                           'observaciones', 'laboratorio', 'tipo_movimiento', 'fecha_vencimiento', 
                           'lote', 'medico', 'junta_vigilancia', 'numero_inscripcion_clinica'])
            writer.writerows(registros)
        
        print(f"Backup creado: {backup_file}")
        return True
        
    except Exception as e:
        print(f"Error al crear backup: {e}")
        return False

def eliminar_productos_obsoletos():
    """Eliminar productos obsoletos del inventario"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener productos con stock 0
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('SELECT COUNT(*) FROM inventario WHERE stock = 0')
        else:
            cursor.execute('SELECT COUNT(*) FROM inventario WHERE stock = 0')
        
        productos_obsoletos = cursor.fetchone()[0]
        
        if productos_obsoletos == 0:
            conn.close()
            return True, "No hay productos obsoletos para eliminar"
        
        # Eliminar productos con stock 0
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('DELETE FROM inventario WHERE stock = 0')
        else:
            cursor.execute('DELETE FROM inventario WHERE stock = 0')
        
        conn.commit()
        conn.close()
        
        return True, f"Se eliminaron {productos_obsoletos} productos obsoletos exitosamente"
        
    except Exception as e:
        return False, f"Error al eliminar productos obsoletos: {str(e)}"

if __name__ == "__main__":
    success, result = eliminar_productos_obsoletos()
    print(result) 