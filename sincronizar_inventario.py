import pandas as pd
import sqlite3
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

def sincronizar_inventario():
    """Sincronizar inventario preservando registros existentes"""
    
    if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
        print("❌ Archivo 'INVENTARIO PARA TRABAJO.csv' no encontrado")
        return False, "Archivo CSV no encontrado"
    
    try:
        # Leer el archivo CSV
        try:
            df = pd.read_csv('INVENTARIO PARA TRABAJO.csv', encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv('INVENTARIO PARA TRABAJO.csv', encoding='latin-1')
            except:
                df = pd.read_csv('INVENTARIO PARA TRABAJO.csv', encoding='cp1252')
        
        # Conectar a la base de datos
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Obtener productos existentes en la base de datos con información completa
        cursor.execute('SELECT id, laboratorio, medicamento, presentacion, stock FROM inventario')
        productos_existentes = {}
        productos_existentes_set = set()
        for row in cursor.fetchall():
            # Crear una clave única para cada producto
            clave = f"{row[1]}|{row[2]}|{row[3]}"
            productos_existentes_set.add(clave)
            productos_existentes[clave] = {
                'id': row[0],
                'laboratorio': row[1],
                'medicamento': row[2],
                'presentacion': row[3],
                'stock': row[4]
            }
        
        print(f"📊 Productos existentes en BD: {len(productos_existentes)}")
        
        # Procesar datos del CSV
        productos_nuevos = []
        productos_actualizados = 0
        productos_en_csv = set()
        categoria_actual = ""
        estadisticas = {
            'productos_existentes': len(productos_existentes),
            'productos_nuevos': 0,
            'productos_actualizados': 0,
            'productos_eliminados': 0,
            'laboratorios': {},
            'categorias': {},
            'productos_eliminados_lista': []
        }
        
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
                
                # Agregar a la lista de productos en CSV
                productos_en_csv.add(clave_producto)
                
                # Verificar si el producto ya existe
                if clave_producto not in productos_existentes_set:
                    productos_nuevos.append({
                        'codigo': codigo,
                        'nombre': nombre_limpio,
                        'presentacion': presentacion,
                        'laboratorio': laboratorio,
                        'categoria': categoria_actual,
                        'precio': 0.0,
                        'stock': 100  # Stock por defecto para productos nuevos
                    })
                    
                    # Actualizar estadísticas
                    estadisticas['productos_nuevos'] += 1
                    estadisticas['laboratorios'][laboratorio] = estadisticas['laboratorios'].get(laboratorio, 0) + 1
                    if categoria_actual:
                        estadisticas['categorias'][categoria_actual] = estadisticas['categorias'].get(categoria_actual, 0) + 1
                else:
                    # Producto existe, verificar si necesita actualización
                    cursor.execute('''
                        SELECT precio, stock FROM inventario 
                        WHERE laboratorio = ? AND medicamento = ? AND presentacion = ?
                    ''', (laboratorio, nombre_limpio, presentacion))
                    
                    resultado = cursor.fetchone()
                    if resultado:
                        precio_actual, stock_actual = resultado
                        # Aquí puedes agregar lógica para actualizar si es necesario
                        productos_actualizados += 1
                        estadisticas['productos_actualizados'] += 1
        
        print(f"🆕 Productos nuevos encontrados: {len(productos_nuevos)}")
        print(f"🔄 Productos existentes: {productos_actualizados}")
        
        # Detectar productos eliminados (están en BD pero no en CSV)
        productos_eliminados = []
        for clave, producto in productos_existentes.items():
            if clave not in productos_en_csv:
                productos_eliminados.append(producto)
                estadisticas['productos_eliminados'] += 1
                estadisticas['productos_eliminados_lista'].append({
                    'laboratorio': producto['laboratorio'],
                    'medicamento': producto['medicamento'],
                    'presentacion': producto['presentacion'],
                    'stock': producto['stock']
                })
        
        print(f"🗑️ Productos eliminados del CSV: {len(productos_eliminados)}")
        
        # Guardar información de productos eliminados para el usuario
        if productos_eliminados:
            print("⚠️ Productos que ya no están en el CSV:")
            for producto in productos_eliminados[:5]:  # Mostrar solo los primeros 5
                print(f"  - {producto['medicamento']} ({producto['laboratorio']})")
            if len(productos_eliminados) > 5:
                print(f"  ... y {len(productos_eliminados) - 5} productos más")
        
        # Insertar solo productos nuevos
        if productos_nuevos:
            for producto in productos_nuevos:
                cursor.execute('''
                    INSERT INTO inventario (laboratorio, medicamento, presentacion, precio, stock)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    producto['laboratorio'],
                    producto['nombre'],
                    producto['presentacion'],
                    producto['precio'],
                    producto['stock']
                ))
            
            conn.commit()
            print(f"✅ {len(productos_nuevos)} productos nuevos agregados exitosamente")
        else:
            print("ℹ️ No se encontraron productos nuevos para agregar")
        
        # Mostrar estadísticas finales
        cursor.execute('SELECT COUNT(*) FROM inventario')
        total_productos = cursor.fetchone()[0]
        print(f"📈 Total de productos en inventario: {total_productos}")
        
        # Mostrar estadísticas por laboratorio
        cursor.execute('''
            SELECT laboratorio, COUNT(*) as cantidad 
            FROM inventario 
            GROUP BY laboratorio 
            ORDER BY cantidad DESC 
            LIMIT 10
        ''')
        
        print("\n🏢 Top 10 Laboratorios:")
        for lab, count in cursor.fetchall():
            print(f"  {lab}: {count} productos")
        
        # Actualizar estadísticas finales
        estadisticas['total_productos'] = total_productos
        estadisticas['productos_nuevos'] = len(productos_nuevos)
        estadisticas['productos_actualizados'] = productos_actualizados
        estadisticas['productos_eliminados'] = len(productos_eliminados)
        
        conn.close()
        return True, estadisticas
        
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
        return False, f"Error: {str(e)}"

def backup_registros():
    """Crear backup de registros antes de sincronizar"""
    try:
        # Crear carpeta backups si no existe
        if not os.path.exists('backups'):
            os.makedirs('backups')
        
        conn = sqlite3.connect('farmacia.db')
        
        # Crear backup con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/backup_registros_{timestamp}.db"
        
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
    print("🔄 Iniciando sincronización de inventario...")
    
    # Crear backup antes de sincronizar
    if backup_registros():
        # Realizar sincronización
        success, result = sincronizar_inventario()
        if success:
            print("\n✅ Sincronización completada exitosamente")
            print(f"📊 Estadísticas: {result}")
        else:
            print(f"\n❌ Error en la sincronización: {result}")
    else:
        print("❌ No se pudo crear el backup, abortando sincronización") 