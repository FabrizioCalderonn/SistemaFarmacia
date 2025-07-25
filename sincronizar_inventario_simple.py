#!/usr/bin/env python3
"""
Script simplificado para sincronizar inventario sin pandas
"""
import os
import csv
from datetime import datetime
import tempfile

# Importar funciones de la aplicación principal
from app import get_db_connection, DATABASE_TYPE

def backup_registros():
    """Crear backup de registros antes de sincronizar"""
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
        backup_file = f"backup_registros_{timestamp}.csv"
        
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

def sincronizar_inventario():
    """Sincronizar inventario desde CSV"""
    try:
        if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
            return False, "Archivo 'INVENTARIO PARA TRABAJO.csv' no encontrado"
        
        # Leer CSV
        inventario_csv = []
        with open('INVENTARIO PARA TRABAJO.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                inventario_csv.append(row)
        
        if not inventario_csv:
            return False, "El archivo CSV está vacío"
        
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Limpiar inventario actual
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('DELETE FROM inventario')
        else:
            cursor.execute('DELETE FROM inventario')
        
        # Insertar nuevos datos
        registros_insertados = 0
        for item in inventario_csv:
            try:
                laboratorio = item.get('laboratorio', '')
                medicamento = item.get('medicamento', '')
                presentacion = item.get('presentacion', '')
                precio = float(item.get('precio', 0))
                stock = int(item.get('stock', 0))
                
                if DATABASE_TYPE == 'postgresql':
                    cursor.execute('''
                        INSERT INTO inventario (laboratorio, medicamento, presentacion, precio, stock)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (laboratorio, medicamento, presentacion, precio, stock))
                else:
                    cursor.execute('''
                        INSERT INTO inventario (laboratorio, medicamento, presentacion, precio, stock)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (laboratorio, medicamento, presentacion, precio, stock))
                
                registros_insertados += 1
                
            except Exception as e:
                print(f"Error al insertar {medicamento}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return True, f"Inventario sincronizado exitosamente. {registros_insertados} registros insertados."
        
    except Exception as e:
        return False, f"Error al sincronizar: {str(e)}"

if __name__ == "__main__":
    success, result = sincronizar_inventario()
    print(result) 