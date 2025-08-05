#!/usr/bin/env python3
"""
Script para verificar que los datos se están guardando correctamente en la base de datos
"""

import sqlite3
from datetime import datetime

def verificar_estructura_datos():
    """Verificar la estructura y datos en la base de datos"""
    print("🔍 VERIFICANDO ESTRUCTURA Y DATOS DE LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Verificar estructura de la tabla
        cursor.execute("PRAGMA table_info(registros)")
        columns = cursor.fetchall()
        
        print("📋 Estructura de la tabla 'registros':")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Default: {col[4]}")
        
        # Obtener algunos registros de ejemplo
        cursor.execute('''
            SELECT laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones,
                   fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica,
                   numero_factura, codigo_empleado, tipo_movimiento
            FROM registros 
            ORDER BY fecha_ingreso DESC
            LIMIT 5
        ''')
        
        registros = cursor.fetchall()
        
        print(f"\n📊 Últimos {len(registros)} registros:")
        for i, registro in enumerate(registros, 1):
            print(f"\n  Registro {i}:")
            print(f"    - Laboratorio: {registro[0]}")
            print(f"    - Medicamento: {registro[1]}")
            print(f"    - Cantidad: {registro[2]}")
            print(f"    - Fecha: {registro[3]}")
            print(f"    - Fecha Ingreso: {registro[4]}")
            print(f"    - Observaciones: {registro[5]}")
            print(f"    - Fecha Vencimiento: {registro[6]}")
            print(f"    - Lote: {registro[7]}")
            print(f"    - Médico: {registro[8]}")
            print(f"    - Junta Vigilancia: {registro[9]}")
            print(f"    - N° Inscripción Clínica: {registro[10]}")
            print(f"    - N° Factura: {registro[11]}")
            print(f"    - Código Empleado: {registro[12]}")
            print(f"    - Tipo Movimiento: {registro[13]}")
            
            # Verificar consistencia
            if registro[13] == 'DEVOLUCION':
                if registro[8] or registro[9] or registro[10]:
                    print(f"    ⚠️  INCONSISTENCIA: Devolución con datos médicos")
                else:
                    print(f"    ✅ Consistente: Devolución sin datos médicos")
            elif registro[13] == 'VENTA':
                if not registro[8] or not registro[9]:
                    print(f"    ⚠️  INCONSISTENCIA: Venta sin datos médicos completos")
                else:
                    print(f"    ✅ Consistente: Venta con datos médicos")
        
        # Verificar distribución de tipos de movimiento
        cursor.execute('''
            SELECT tipo_movimiento, COUNT(*) as cantidad
            FROM registros 
            GROUP BY tipo_movimiento
        ''')
        
        distribucion = cursor.fetchall()
        
        print(f"\n📈 Distribución de tipos de movimiento:")
        for tipo, cantidad in distribucion:
            print(f"  - {tipo}: {cantidad} registros")
        
        # Verificar códigos de empleado
        cursor.execute('''
            SELECT codigo_empleado, COUNT(*) as cantidad
            FROM registros 
            WHERE codigo_empleado IS NOT NULL AND codigo_empleado != ''
            GROUP BY codigo_empleado
            ORDER BY cantidad DESC
            LIMIT 10
        ''')
        
        empleados = cursor.fetchall()
        
        print(f"\n👥 Códigos de empleado más usados:")
        for empleado, cantidad in empleados:
            print(f"  - {empleado}: {cantidad} registros")
        
        conn.close()
        
        print(f"\n✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar datos: {e}")
        return False

def corregir_datos_inconsistentes():
    """Corregir datos inconsistentes en la base de datos"""
    print("\n🔧 CORRIGIENDO DATOS INCONSISTENTES")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Buscar registros donde tipo_movimiento es 'DEVOLUCION' pero tiene datos médicos
        cursor.execute('''
            SELECT id, tipo_movimiento, medico, junta_vigilancia, numero_inscripcion_clinica
            FROM registros 
            WHERE tipo_movimiento = 'DEVOLUCION' 
            AND (medico IS NOT NULL AND medico != '' 
                 OR junta_vigilancia IS NOT NULL AND junta_vigilancia != ''
                 OR numero_inscripcion_clinica IS NOT NULL AND numero_inscripcion_clinica != '')
        ''')
        
        inconsistencias = cursor.fetchall()
        
        if inconsistencias:
            print(f"🔍 Encontradas {len(inconsistencias)} inconsistencias:")
            for reg in inconsistencias:
                print(f"  - ID {reg[0]}: Tipo={reg[1]}, Médico={reg[2]}, Junta={reg[3]}, Inscripción={reg[4]}")
            
            # Corregir limpiando datos médicos en devoluciones
            cursor.execute('''
                UPDATE registros 
                SET medico = '', junta_vigilancia = '', numero_inscripcion_clinica = ''
                WHERE tipo_movimiento = 'DEVOLUCION' 
                AND (medico IS NOT NULL AND medico != '' 
                     OR junta_vigilancia IS NOT NULL AND junta_vigilancia != ''
                     OR numero_inscripcion_clinica IS NOT NULL AND numero_inscripcion_clinica != '')
            ''')
            
            conn.commit()
            print(f"✅ Corregidas {len(inconsistencias)} inconsistencias")
        else:
            print("✅ No se encontraron inconsistencias")
        
        # Buscar registros donde tipo_movimiento es 'VENTA' pero no tiene datos médicos
        cursor.execute('''
            SELECT id, tipo_movimiento, medico, junta_vigilancia
            FROM registros 
            WHERE tipo_movimiento = 'VENTA' 
            AND (medico IS NULL OR medico = '' OR junta_vigilancia IS NULL OR junta_vigilancia = '')
        ''')
        
        ventas_incompletas = cursor.fetchall()
        
        if ventas_incompletas:
            print(f"⚠️  Encontradas {len(ventas_incompletas)} ventas con datos médicos incompletos:")
            for reg in ventas_incompletas:
                print(f"  - ID {reg[0]}: Tipo={reg[1]}, Médico={reg[2]}, Junta={reg[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al corregir datos: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 VERIFICACIÓN Y CORRECCIÓN DE DATOS")
    print("=" * 60)
    
    # Verificar estructura y datos
    if not verificar_estructura_datos():
        return
    
    # Corregir inconsistencias
    if not corregir_datos_inconsistentes():
        return
    
    print("\n🎉 ¡Verificación y corrección completadas!")
    print("Los datos ahora deberían estar consistentes.")

if __name__ == "__main__":
    main() 