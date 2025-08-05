#!/usr/bin/env python3
"""
Script de prueba para verificar las funcionalidades de ventas y devoluciones
"""

import sqlite3
import json
from datetime import datetime

def test_database_structure():
    """Probar la estructura de la base de datos"""
    print("🔍 Probando estructura de la base de datos...")
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Verificar que la tabla registros existe y tiene el campo tipo_movimiento
        cursor.execute("PRAGMA table_info(registros)")
        columns = cursor.fetchall()
        
        tipo_movimiento_exists = False
        for col in columns:
            if col[1] == 'tipo_movimiento':
                tipo_movimiento_exists = True
                print(f"✅ Campo 'tipo_movimiento' encontrado: {col}")
                break
        
        if not tipo_movimiento_exists:
            print("❌ Campo 'tipo_movimiento' no encontrado en la tabla registros")
            return False
        
        print("✅ Estructura de base de datos correcta")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar estructura de base de datos: {e}")
        return False

def test_insert_venta():
    """Probar inserción de una venta"""
    print("\n💰 Probando inserción de venta...")
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Datos de prueba para venta
        venta_data = {
            'laboratorio': 'Laboratorio Test',
            'medicamento': 'Medicamento Test',
            'cantidad': 5,
            'fecha': '2024-01-15',
            'fecha_ingreso': datetime.now().isoformat(),
            'observaciones': 'Venta de prueba',
            'tipo_movimiento': 'VENTA',
            'fecha_vencimiento': '2025-12-31',
            'lote': 'LOTE001',
            'medico': 'Dr. Test',
            'junta_vigilancia': 'JV001',
            'numero_inscripcion_clinica': 'NIC001',
            'numero_factura': 'FAC001',
            'codigo_empleado': 'EMP001',
            'farmacia': 'farmacia1'
        }
        
        cursor.execute('''
            INSERT INTO registros (laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones, tipo_movimiento, 
                                 fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica, numero_factura, codigo_empleado, farmacia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            venta_data['laboratorio'],
            venta_data['medicamento'],
            venta_data['cantidad'],
            venta_data['fecha'],
            venta_data['fecha_ingreso'],
            venta_data['observaciones'],
            venta_data['tipo_movimiento'],
            venta_data['fecha_vencimiento'],
            venta_data['lote'],
            venta_data['medico'],
            venta_data['junta_vigilancia'],
            venta_data['numero_inscripcion_clinica'],
            venta_data['numero_factura'],
            venta_data['codigo_empleado'],
            venta_data['farmacia']
        ))
        
        conn.commit()
        print("✅ Venta insertada correctamente")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al insertar venta: {e}")
        return False

def test_insert_devolucion():
    """Probar inserción de una devolución"""
    print("\n↩️ Probando inserción de devolución...")
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Datos de prueba para devolución
        devolucion_data = {
            'laboratorio': 'Laboratorio Test',
            'medicamento': 'Medicamento Test',
            'cantidad': 2,
            'fecha': '2024-01-15',
            'fecha_ingreso': datetime.now().isoformat(),
            'observaciones': 'Devolución de prueba - producto defectuoso',
            'tipo_movimiento': 'DEVOLUCION',
            'fecha_vencimiento': '2025-12-31',
            'lote': 'LOTE001',
            'medico': '',  # No requerido para devoluciones
            'junta_vigilancia': '',  # No requerido para devoluciones
            'numero_inscripcion_clinica': '',  # No requerido para devoluciones
            'numero_factura': 'DEV001',
            'codigo_empleado': 'EMP001',
            'farmacia': 'farmacia1'
        }
        
        cursor.execute('''
            INSERT INTO registros (laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones, tipo_movimiento, 
                                 fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica, numero_factura, codigo_empleado, farmacia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            devolucion_data['laboratorio'],
            devolucion_data['medicamento'],
            devolucion_data['cantidad'],
            devolucion_data['fecha'],
            devolucion_data['fecha_ingreso'],
            devolucion_data['observaciones'],
            devolucion_data['tipo_movimiento'],
            devolucion_data['fecha_vencimiento'],
            devolucion_data['lote'],
            devolucion_data['medico'],
            devolucion_data['junta_vigilancia'],
            devolucion_data['numero_inscripcion_clinica'],
            devolucion_data['numero_factura'],
            devolucion_data['codigo_empleado'],
            devolucion_data['farmacia']
        ))
        
        conn.commit()
        print("✅ Devolución insertada correctamente")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al insertar devolución: {e}")
        return False

def test_query_registros():
    """Probar consulta de registros con tipo_movimiento"""
    print("\n📊 Probando consulta de registros...")
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Consultar registros con tipo_movimiento
        cursor.execute('''
            SELECT id, laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones,
                   fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica, numero_factura, codigo_empleado, tipo_movimiento
            FROM registros 
            WHERE farmacia = ?
            ORDER BY fecha_ingreso DESC
        ''', ('farmacia1',))
        
        registros = cursor.fetchall()
        
        print(f"✅ Se encontraron {len(registros)} registros")
        
        # Mostrar algunos registros de ejemplo
        for i, reg in enumerate(registros[:3]):
            print(f"  Registro {i+1}:")
            print(f"    - Medicamento: {reg[2]}")
            print(f"    - Cantidad: {reg[3]}")
            print(f"    - Tipo: {reg[14] if len(reg) > 14 else 'VENTA'}")
            print(f"    - N° Factura/Devolución: {reg[12] if len(reg) > 12 else ''}")
            print()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al consultar registros: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 INICIANDO PRUEBAS DE VENTAS Y DEVOLUCIONES")
    print("=" * 50)
    
    # Ejecutar pruebas
    tests = [
        test_database_structure,
        test_insert_venta,
        test_insert_devolucion,
        test_query_registros
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Error en prueba {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📈 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar los errores anteriores.")

if __name__ == "__main__":
    main() 