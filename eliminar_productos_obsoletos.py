import sqlite3
import pandas as pd
import re
import os
from datetime import datetime

def limpiar_texto(texto):
    """Limpiar texto de caracteres especiales y espacios extra"""
    if pd.isna(texto):
        return ""
    texto = str(texto).strip()
    # Remover caracteres especiales y espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def obtener_productos_csv():
    """Obtener lista de productos del archivo CSV"""
    if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
        return set()
    
    try:
        # Leer el archivo CSV
        try:
            df = pd.read_csv('INVENTARIO PARA TRABAJO.csv', encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv('INVENTARIO PARA TRABAJO.csv', encoding='latin-1')
            except:
                df = pd.read_csv('INVENTARIO PARA TRABAJO.csv', encoding='cp1252')
        
        productos_csv = set()
        categoria_actual = ""
        
        for index, row in df.iterrows():
            # Obtener valores de las columnas
            codigo = limpiar_texto(row.iloc[0]) if len(row) > 0 else ""
            nombre = limpiar_texto(row.iloc[1]) if len(row) > 1 else ""
            modelo = limpiar_texto(row.iloc[2]) if len(row) > 2 else ""
            marca = limpiar_texto(row.iloc[3]) if len(row) > 3 else ""
            
            # Verificar si es una línea de categoría
            if codigo and not re.match(r'^\d{6}', codigo) and 'CONVENIENCIA' in codigo:
                categoria_actual = codigo
                continue
            
            # Verificar si es un producto válido
            if (codigo and re.match(r'^\d{9}', codigo) and 
                nombre and len(nombre) > 5 and 
                marca and marca != ""):
                
                # Limpiar datos
                nombre_limpio = nombre.strip()
                laboratorio = marca if marca and marca != "" else "VARIOS"
                presentacion = modelo if modelo else f"Código: {codigo}"
                
                # Crear clave única para el producto
                clave_producto = f"{laboratorio}|{nombre_limpio}|{presentacion}"
                productos_csv.add(clave_producto)
        
        return productos_csv
        
    except Exception as e:
        print(f"Error al leer CSV: {e}")
        return set()

def eliminar_productos_obsoletos():
    """Eliminar productos que ya no están en el CSV"""
    
    # Obtener productos del CSV
    productos_csv = obtener_productos_csv()
    if not productos_csv:
        print("❌ No se pudieron obtener productos del CSV")
        return False, "No se pudieron obtener productos del CSV"
    
    try:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Obtener productos de la base de datos
        cursor.execute('SELECT id, laboratorio, medicamento, presentacion, stock FROM inventario')
        productos_bd = cursor.fetchall()
        
        productos_a_eliminar = []
        estadisticas = {
            'total_productos_bd': len(productos_bd),
            'productos_eliminados': 0,
            'productos_con_stock': 0,
            'productos_sin_stock': 0,
            'laboratorios_afectados': {}
        }
        
        # Identificar productos a eliminar
        for producto in productos_bd:
            id_producto, laboratorio, medicamento, presentacion, stock = producto
            clave_producto = f"{laboratorio}|{medicamento}|{presentacion}"
            
            if clave_producto not in productos_csv:
                productos_a_eliminar.append({
                    'id': id_producto,
                    'laboratorio': laboratorio,
                    'medicamento': medicamento,
                    'presentacion': presentacion,
                    'stock': stock
                })
                
                estadisticas['productos_eliminados'] += 1
                if stock > 0:
                    estadisticas['productos_con_stock'] += 1
                else:
                    estadisticas['productos_sin_stock'] += 1
                
                estadisticas['laboratorios_afectados'][laboratorio] = estadisticas['laboratorios_afectados'].get(laboratorio, 0) + 1
        
        if not productos_a_eliminar:
            print("✅ No hay productos obsoletos para eliminar")
            conn.close()
            return True, "No hay productos obsoletos para eliminar"
        
        # Mostrar resumen antes de eliminar
        print(f"🗑️ Productos a eliminar: {len(productos_a_eliminar)}")
        print(f"  - Con stock: {estadisticas['productos_con_stock']}")
        print(f"  - Sin stock: {estadisticas['productos_sin_stock']}")
        
        # Eliminar productos
        for producto in productos_a_eliminar:
            cursor.execute('DELETE FROM inventario WHERE id = ?', (producto['id'],))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(productos_a_eliminar)} productos eliminados exitosamente")
        return True, estadisticas
        
    except Exception as e:
        print(f"❌ Error al eliminar productos: {e}")
        return False, f"Error: {str(e)}"

def backup_antes_de_eliminar():
    """Crear backup antes de eliminar productos"""
    try:
        # Crear carpeta backups si no existe
        if not os.path.exists('backups'):
            os.makedirs('backups')
        
        conn = sqlite3.connect('farmacia.db')
        
        # Crear backup con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/backup_antes_eliminacion_{timestamp}.db"
        
        # Crear conexión al archivo de backup
        backup_conn = sqlite3.connect(backup_file)
        
        # Copiar registros al backup
        conn.backup(backup_conn)
        
        backup_conn.close()
        conn.close()
        
        print(f"💾 Backup creado: {backup_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

if __name__ == "__main__":
    print("🗑️ Iniciando eliminación de productos obsoletos...")
    
    # Crear backup antes de eliminar
    if backup_antes_de_eliminar():
        # Realizar eliminación
        success, result = eliminar_productos_obsoletos()
        if success:
            print("\n✅ Eliminación completada exitosamente")
            if isinstance(result, dict):
                print(f"📊 Estadísticas: {result}")
        else:
            print(f"\n❌ Error en la eliminación: {result}")
    else:
        print("❌ No se pudo crear el backup, abortando eliminación") 