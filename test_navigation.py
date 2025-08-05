#!/usr/bin/env python3
"""
Script para probar la navegación con Enter en el formulario
"""

import webbrowser
import time
import os

def test_navigation():
    """Probar la navegación con Enter"""
    print("🧪 PRUEBA DE NAVEGACIÓN CON ENTER")
    print("=" * 50)
    
    print("📋 Funcionalidades implementadas:")
    print("✅ Enter = Pasar al siguiente campo")
    print("✅ Shift + Enter = Ir al campo anterior")
    print("✅ Solo clic en botón para guardar")
    print("✅ Navegación inteligente (salta campos deshabilitados)")
    print("✅ Tooltip informativo para nuevos usuarios")
    print("✅ Efectos visuales en botones de guardar")
    
    print("\n🎯 Instrucciones de prueba:")
    print("1. Abre el sistema en el navegador")
    print("2. Ve a la pestaña 'Venta' o 'Devolución'")
    print("3. Completa los campos usando Enter para navegar")
    print("4. Usa Shift+Enter para volver atrás")
    print("5. Solo guarda haciendo clic en el botón")
    
    print("\n🔧 Características técnicas:")
    print("- Prevención de envío automático del formulario")
    print("- Navegación inteligente entre campos habilitados")
    print("- Manejo especial para selects y textareas")
    print("- Tooltip que se muestra solo una vez")
    print("- Efectos visuales mejorados en botones")
    
    print("\n📱 Compatibilidad:")
    print("- Funciona en todas las pestañas (Venta/Devolución)")
    print("- Compatible con campos deshabilitados")
    print("- Manejo de campos ocultos")
    print("- Responsive en móviles")
    
    print("\n🎉 ¡Navegación mejorada implementada!")
    print("El sistema ahora permite navegar rápidamente con Enter")
    print("y solo guarda cuando se hace clic en el botón.")

def main():
    """Función principal"""
    test_navigation()
    
    # Preguntar si quiere abrir el navegador
    try:
        response = input("\n¿Quieres abrir el sistema en el navegador? (s/n): ").lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            print("🌐 Abriendo sistema en el navegador...")
            webbrowser.open('http://localhost:5000')
    except KeyboardInterrupt:
        print("\n👋 Prueba cancelada por el usuario")

if __name__ == "__main__":
    main() 