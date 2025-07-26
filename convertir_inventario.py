#!/usr/bin/env python3
"""
Script para convertir el archivo de inventario a formato CSV estándar
"""
import csv
import os

def convertir_a_csv_estandar():
    """Convertir el archivo de inventario a CSV estándar"""
    try:
        # Leer el archivo original
        with open('INVENTARIO PARA TRABAJO.csv', 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        
        # Crear archivo CSV estándar
        with open('inventario_estandar.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir encabezados
            writer.writerow(['codigo', 'nombre', 'modelo', 'laboratorio', 'precio', 'stock'])
            
            # Buscar línea de encabezados
            header_found = False
            for line in lines:
                line = line.strip()
                
                # Detectar línea de encabezados
                if 'Codigo' in line and 'Nombre' in line:
                    header_found = True
                    continue
                
                # Procesar líneas de datos
                if header_found and line and not line.startswith('"Listado') and not line.startswith('"Reportes'):
                    # Limpiar la línea
                    line = line.replace('"', '')
                    parts = [part.strip() for part in line.split('\t') if part.strip()]
                    
                    if len(parts) >= 3:
                        codigo = parts[0]
                        nombre = parts[1]
                        modelo_marca = parts[2]
                        
                        # Extraer modelo y laboratorio
                        if ',' in modelo_marca:
                            modelo, laboratorio = modelo_marca.rsplit(',', 1)
                            modelo = modelo.strip()
                            laboratorio = laboratorio.strip()
                        else:
                            modelo = modelo_marca.strip()
                            laboratorio = 'Sin especificar'
                        
                        # Solo agregar si tiene código y nombre válidos
                        if codigo and nombre and len(codigo.strip()) > 3 and len(nombre.strip()) > 3:
                            writer.writerow([
                                codigo.strip(),
                                nombre.strip(),
                                modelo,
                                laboratorio,
                                0.0,  # precio por defecto
                                1     # stock por defecto
                            ])
        
        print("Archivo convertido exitosamente: inventario_estandar.csv")
        return True
        
    except Exception as e:
        print(f"Error al convertir: {e}")
        return False

if __name__ == "__main__":
    convertir_a_csv_estandar() 