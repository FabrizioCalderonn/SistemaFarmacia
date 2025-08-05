#!/usr/bin/env python3
"""
Script para actualizar la estructura de la base de datos
"""

import sqlite3
from datetime import datetime

def actualizar_estructura_db():
    """Actualizar la estructura de la base de datos"""
    print("🔧 Actualizando estructura de la base de datos...")
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Verificar estructura actual
        cursor.execute("PRAGMA table_info(registros)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Columnas actuales:", column_names)
        
        # Campos que deberían existir
        campos_requeridos = [
            'id', 'laboratorio', 'medicamento', 'cantidad', 'fecha', 
            'fecha_ingreso', 'observaciones', 'tipo_movimiento',
            'fecha_vencimiento', 'lote', 'medico', 'junta_vigilancia',
            'numero_inscripcion_clinica', 'numero_factura', 'codigo_empleado', 'farmacia'
        ]
        
        # Agregar campos faltantes
        campos_faltantes = []
        for campo in campos_requeridos:
            if campo not in column_names:
                campos_faltantes.append(campo)
        
        if campos_faltantes:
            print(f"Campos faltantes: {campos_faltantes}")
            
            # Agregar campos uno por uno
            for campo in campos_faltantes:
                try:
                    if campo == 'numero_factura':
                        cursor.execute("ALTER TABLE registros ADD COLUMN numero_factura TEXT")
                        print(f"✅ Agregado campo: {campo}")
                    elif campo == 'codigo_empleado':
                        cursor.execute("ALTER TABLE registros ADD COLUMN codigo_empleado TEXT")
                        print(f"✅ Agregado campo: {campo}")
                    elif campo == 'farmacia':
                        cursor.execute("ALTER TABLE registros ADD COLUMN farmacia TEXT DEFAULT 'farmacia1'")
                        print(f"✅ Agregado campo: {campo}")
                    elif campo == 'tipo_movimiento':
                        cursor.execute("ALTER TABLE registros ADD COLUMN tipo_movimiento TEXT DEFAULT 'VENTA'")
                        print(f"✅ Agregado campo: {campo}")
                    else:
                        cursor.execute(f"ALTER TABLE registros ADD COLUMN {campo} TEXT")
                        print(f"✅ Agregado campo: {campo}")
                except Exception as e:
                    print(f"⚠️ Error al agregar campo {campo}: {e}")
        else:
            print("✅ Todos los campos requeridos ya existen")
        
        conn.commit()
        
        # Verificar estructura final
        cursor.execute("PRAGMA table_info(registros)")
        columns_final = cursor.fetchall()
        print("\nEstructura final de la tabla registros:")
        for col in columns_final:
            print(f"  {col[1]} ({col[2]}) - Default: {col[4]}")
        
        conn.close()
        print("\n✅ Estructura de base de datos actualizada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar estructura: {e}")
        return False

def crear_tabla_si_no_existe():
    """Crear la tabla registros si no existe"""
    print("🏗️ Verificando si la tabla registros existe...")
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                laboratorio TEXT NOT NULL,
                medicamento TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL,
                observaciones TEXT,
                tipo_movimiento TEXT DEFAULT 'VENTA',
                fecha_vencimiento TEXT,
                lote TEXT,
                medico TEXT,
                junta_vigilancia TEXT,
                numero_inscripcion_clinica TEXT,
                numero_factura TEXT,
                codigo_empleado TEXT,
                farmacia TEXT DEFAULT 'farmacia1'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Tabla registros creada/verificada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 ACTUALIZADOR DE BASE DE DATOS")
    print("=" * 40)
    
    # Crear tabla si no existe
    if not crear_tabla_si_no_existe():
        return
    
    # Actualizar estructura
    if not actualizar_estructura_db():
        return
    
    print("\n🎉 ¡Base de datos actualizada correctamente!")
    print("Ahora puedes ejecutar el sistema con las nuevas funcionalidades.")

if __name__ == "__main__":
    main() 