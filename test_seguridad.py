#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de seguridad del sistema
"""

import requests
import json
import sys
import os

# Configuración de prueba
BASE_URL = "http://localhost:5000"
TEST_PASSWORD = "admin123"  # Contraseña por defecto

def test_eliminacion_sin_password():
    """Probar eliminación sin contraseña (debe fallar)"""
    print("🔒 Probando eliminación sin contraseña...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/registros/999", 
                                headers={'Content-Type': 'application/json'})
        
        if response.status_code == 400:
            data = response.json()
            if "Contraseña de administrador requerida" in data.get('message', ''):
                print("✅ Test pasado: Eliminación sin contraseña correctamente rechazada")
                return True
            else:
                print(f"❌ Test falló: Mensaje inesperado: {data.get('message')}")
                return False
        else:
            print(f"❌ Test falló: Status code inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test falló con error: {e}")
        return False

def test_eliminacion_password_incorrecto():
    """Probar eliminación con contraseña incorrecta (debe fallar)"""
    print("🔒 Probando eliminación con contraseña incorrecta...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/registros/999", 
                                headers={'Content-Type': 'application/json'},
                                json={'password': 'password_incorrecta'})
        
        if response.status_code == 400:
            data = response.json()
            if "Contraseña de administrador incorrecta" in data.get('message', ''):
                print("✅ Test pasado: Eliminación con contraseña incorrecta correctamente rechazada")
                return True
            else:
                print(f"❌ Test falló: Mensaje inesperado: {data.get('message')}")
                return False
        else:
            print(f"❌ Test falló: Status code inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test falló con error: {e}")
        return False

def test_eliminacion_password_correcto():
    """Probar eliminación con contraseña correcta (puede fallar si no hay registros)"""
    print("🔒 Probando eliminación con contraseña correcta...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/registros/999", 
                                headers={'Content-Type': 'application/json'},
                                json={'password': TEST_PASSWORD})
        
        data = response.json()
        
        if response.status_code == 400 and "Registro no encontrado" in data.get('message', ''):
            print("✅ Test pasado: Contraseña aceptada, pero registro no encontrado (esperado)")
            return True
        elif response.status_code == 200 and data.get('success'):
            print("✅ Test pasado: Eliminación exitosa con contraseña correcta")
            return True
        else:
            print(f"❌ Test falló: Respuesta inesperada: {data}")
            return False
            
    except Exception as e:
        print(f"❌ Test falló con error: {e}")
        return False

def test_configuracion():
    """Verificar que la configuración se carga correctamente"""
    print("⚙️ Verificando configuración...")
    
    try:
        # Importar configuración
        from config import Config
        
        print(f"   Contraseña de admin configurada: {'Sí' if Config.ADMIN_PASSWORD else 'No'}")
        print(f"   Clave secreta configurada: {'Sí' if Config.SECRET_KEY else 'No'}")
        print(f"   Tipo de base de datos: {Config.DATABASE_TYPE}")
        print(f"   Farmacias configuradas: {len(Config.FARMACIAS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar configuración: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🔐 Iniciando pruebas de seguridad del Sistema de Farmacia")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print(f"❌ Error: El servidor no responde correctamente (Status: {response.status_code})")
            print("   Asegúrese de que la aplicación esté corriendo en http://localhost:5000")
            return False
    except Exception as e:
        print(f"❌ Error: No se puede conectar al servidor: {e}")
        print("   Asegúrese de que la aplicación esté corriendo en http://localhost:5000")
        return False
    
    print("✅ Servidor respondiendo correctamente")
    print()
    
    # Ejecutar pruebas
    tests = [
        test_configuracion,
        test_eliminacion_sin_password,
        test_eliminacion_password_incorrecto,
        test_eliminacion_password_correcto
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} falló con excepción: {e}")
        print()
    
    # Resumen
    print("=" * 60)
    print(f"📊 Resumen de pruebas: {passed}/{total} pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas de seguridad pasaron exitosamente!")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revise la configuración.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
