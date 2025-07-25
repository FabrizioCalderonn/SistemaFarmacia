#!/usr/bin/env python3
"""
Script para hacer backup automático de la base de datos SQLite
"""

import sqlite3
import shutil
import os
from datetime import datetime
import zipfile

def hacer_backup():
    """Crear backup de la base de datos"""
    
    # Configuración
    db_original = 'farmacia.db'
    carpeta_backups = './backups'
    
    # Crear carpeta de backups si no existe
    if not os.path.exists(carpeta_backups):
        os.makedirs(carpeta_backups)
        print(f"📁 Carpeta '{carpeta_backups}' creada")
    
    # Generar nombre del backup con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"farmacia_backup_{timestamp}.db"
    backup_path = os.path.join(carpeta_backups, backup_file)
    
    try:
        # Verificar que la base de datos existe
        if not os.path.exists(db_original):
            print(f"❌ Error: No se encontró '{db_original}'")
            return False
        
        # Crear backup
        shutil.copy2(db_original, backup_path)
        
        # Crear backup comprimido
        zip_file = f"farmacia_backup_{timestamp}.zip"
        zip_path = os.path.join(carpeta_backups, zip_file)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(backup_path, os.path.basename(backup_path))
        
        # Eliminar archivo .db del backup (mantener solo el .zip)
        os.remove(backup_path)
        
        print(f"✅ Backup creado exitosamente!")
        print(f"📁 Archivo: {zip_path}")
        print(f"📊 Tamaño: {os.path.getsize(zip_path) / 1024:.1f} KB")
        
        # Mostrar estadísticas de la base de datos
        mostrar_estadisticas(db_original)
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def restaurar_backup(backup_file):
    """Restaurar base de datos desde un backup"""
    
    try:
        # Extraer backup
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall('temp_backup')
        
        # Buscar archivo .db extraído
        for file in os.listdir('temp_backup'):
            if file.endswith('.db'):
                db_file = os.path.join('temp_backup', file)
                break
        else:
            print("❌ No se encontró archivo .db en el backup")
            return False
        
        # Crear backup del archivo actual antes de restaurar
        if os.path.exists('farmacia.db'):
            # Crear carpeta backups si no existe
            if not os.path.exists('backups'):
                os.makedirs('backups')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2('farmacia.db', f'backups/farmacia_antes_restauracion_{timestamp}.db')
        
        # Restaurar
        shutil.copy2(db_file, 'farmacia.db')
        
        # Limpiar archivos temporales
        shutil.rmtree('temp_backup')
        
        print(f"✅ Backup restaurado exitosamente desde: {backup_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error al restaurar backup: {e}")
        return False

def mostrar_estadisticas(db_file):
    """Mostrar estadísticas de la base de datos"""
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Contar registros en inventario
        cursor.execute("SELECT COUNT(*) FROM inventario")
        total_inventario = cursor.fetchone()[0]
        
        # Contar registros en registros
        cursor.execute("SELECT COUNT(*) FROM registros")
        total_registros = cursor.fetchone()[0]
        
        # Contar laboratorios únicos
        cursor.execute("SELECT COUNT(DISTINCT laboratorio) FROM inventario")
        laboratorios = cursor.fetchone()[0]
        
        # Valor total de registros
        cursor.execute("SELECT SUM(cantidad * precio) FROM registros")
        valor_total = cursor.fetchone()[0] or 0
        
        conn.close()
        
        print(f"\n📊 Estadísticas de la Base de Datos:")
        print(f"   🏭 Laboratorios: {laboratorios}")
        print(f"   💊 Medicamentos en inventario: {total_inventario}")
        print(f"   📝 Registros totales: {total_registros}")
        print(f"   💰 Valor total: ${valor_total:.2f}")
        
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")

def listar_backups():
    """Listar todos los backups disponibles"""
    
    carpeta_backups = 'backups'
    
    if not os.path.exists(carpeta_backups):
        print("📁 No hay carpeta de backups")
        return
    
    backups = [f for f in os.listdir(carpeta_backups) if f.endswith('.zip')]
    
    if not backups:
        print("📁 No hay backups disponibles")
        return
    
    print(f"\n📁 Backups disponibles ({len(backups)}):")
    for i, backup in enumerate(sorted(backups, reverse=True), 1):
        backup_path = os.path.join(carpeta_backups, backup)
        size = os.path.getsize(backup_path) / 1024
        print(f"   {i}. {backup} ({size:.1f} KB)")

if __name__ == '__main__':
    print("🏥 Sistema de Farmacia - Gestión de Backups")
    print("=" * 50)
    print()
    print("Elige una opción:")
    print("1. Crear backup")
    print("2. Listar backups")
    print("3. Restaurar backup")
    print("4. Mostrar estadísticas")
    print()
    
    try:
        opcion = input("Opción (1-4): ").strip()
        
        if opcion == '1':
            hacer_backup()
        elif opcion == '2':
            listar_backups()
        elif opcion == '3':
            listar_backups()
            print()
            backup_file = input("Nombre del archivo de backup a restaurar: ").strip()
            if backup_file:
                restaurar_backup(os.path.join('backups', backup_file))
        elif opcion == '4':
            mostrar_estadisticas('farmacia.db')
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada") 