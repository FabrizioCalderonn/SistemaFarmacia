import sqlite3
import os
import shutil
from datetime import datetime, timedelta

def crear_backup_automatico():
    """Crear backup automático de la base de datos"""
    try:
        # Crear directorio de backups si no existe
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Crear backup con fecha
        fecha = datetime.now().strftime("%Y%m%d")
        backup_file = f"{backup_dir}/farmacia_backup_{fecha}.db"
        
        # Copiar base de datos
        shutil.copy2('farmacia.db', backup_file)
        
        print(f"✅ Backup automático creado: {backup_file}")
        
        # Limpiar backups antiguos (mantener solo los últimos 7 días)
        limpiar_backups_antiguos(backup_dir, 7)
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear backup automático: {e}")
        return False

def limpiar_backups_antiguos(backup_dir, dias_a_mantener):
    """Eliminar backups más antiguos que el número de días especificado"""
    try:
        fecha_limite = datetime.now() - timedelta(days=dias_a_mantener)
        
        for archivo in os.listdir(backup_dir):
            if archivo.startswith("farmacia_backup_") and archivo.endswith(".db"):
                ruta_archivo = os.path.join(backup_dir, archivo)
                fecha_archivo = os.path.getctime(ruta_archivo)
                fecha_archivo_dt = datetime.fromtimestamp(fecha_archivo)
                
                if fecha_archivo_dt < fecha_limite:
                    os.remove(ruta_archivo)
                    print(f"🗑️ Backup eliminado: {archivo}")
                    
    except Exception as e:
        print(f"❌ Error al limpiar backups antiguos: {e}")

def verificar_integridad_bd():
    """Verificar la integridad de la base de datos"""
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Verificar integridad
        cursor.execute("PRAGMA integrity_check")
        resultado = cursor.fetchone()
        
        if resultado[0] == "ok":
            print("✅ Integridad de la base de datos: OK")
            conn.close()
            return True
        else:
            print(f"❌ Problemas de integridad: {resultado[0]}")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar integridad: {e}")
        return False

def optimizar_bd():
    """Optimizar la base de datos"""
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Analizar tablas
        cursor.execute("ANALYZE")
        
        # Optimizar
        cursor.execute("VACUUM")
        
        # Reindexar
        cursor.execute("REINDEX")
        
        conn.close()
        print("✅ Base de datos optimizada")
        return True
        
    except Exception as e:
        print(f"❌ Error al optimizar BD: {e}")
        return False

def generar_reporte_mantenimiento():
    """Generar reporte de mantenimiento"""
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Estadísticas de la base de datos
        cursor.execute("SELECT COUNT(*) FROM inventario")
        total_productos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM registros")
        total_registros = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT laboratorio) FROM inventario")
        total_laboratorios = cursor.fetchone()[0]
        
        # Tamaño de la base de datos
        tamano_bd = os.path.getsize('farmacia.db') / (1024 * 1024)  # MB
        
        conn.close()
        
        # Generar reporte
        reporte = f"""
📊 REPORTE DE MANTENIMIENTO - {datetime.now().strftime("%d/%m/%Y %H:%M")}
═══════════════════════════════════════════════════════════════════════════════

📦 Inventario:
   • Total productos: {total_productos:,}
   • Total laboratorios: {total_laboratorios}
   • Productos sin stock: {total_productos - total_registros}

📋 Registros:
   • Total registros: {total_registros:,}
   • Promedio por producto: {total_registros/total_productos:.1f if total_productos > 0 else 0}

💾 Base de datos:
   • Tamaño: {tamano_bd:.2f} MB
   • Integridad: {'✅ OK' if verificar_integridad_bd() else '❌ PROBLEMAS'}

🔄 Mantenimiento:
   • Backup automático: {'✅ Creado' if crear_backup_automatico() else '❌ Error'}
   • Optimización: {'✅ Completada' if optimizar_bd() else '❌ Error'}

═══════════════════════════════════════════════════════════════════════════════
        """
        
        # Guardar reporte
        with open(f"reporte_mantenimiento_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "w", encoding="utf-8") as f:
            f.write(reporte)
        
        print(reporte)
        return True
        
    except Exception as e:
        print(f"❌ Error al generar reporte: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Iniciando mantenimiento automático...")
    
    # Ejecutar mantenimiento
    generar_reporte_mantenimiento()
    
    print("\n✅ Mantenimiento completado") 