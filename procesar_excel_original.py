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

def procesar_excel_original(archivo_excel):
    """Procesar archivo Excel original y convertirlo al formato necesario"""
    
    if not os.path.exists(archivo_excel):
        print(f"❌ Archivo '{archivo_excel}' no encontrado")
        return False, f"Archivo '{archivo_excel}' no encontrado"
    
    try:
        # Leer el archivo Excel
        print(f"📖 Leyendo archivo Excel: {archivo_excel}")
        df = pd.read_excel(archivo_excel)
        
        print(f"📊 Columnas encontradas: {list(df.columns)}")
        print(f"📈 Filas encontradas: {len(df)}")
        
        # Mostrar las primeras filas para entender la estructura
        print("\n🔍 Primeras 5 filas del archivo:")
        print(df.head())
        
        # Procesar datos del Excel
        productos = []
        categoria_actual = ""
        
        for index, row in df.iterrows():
            # Obtener valores de las columnas según la estructura del Excel
            codigo = limpiar_texto(row.iloc[0]) if len(row) > 0 else ""
            nombre = limpiar_texto(row.iloc[1]) if len(row) > 1 else ""  # medicamento
            cantidad = limpiar_texto(row.iloc[2]) if len(row) > 2 else ""  # cantidad (no usar)
            unidad = limpiar_texto(row.iloc[3]) if len(row) > 3 else ""   # unidad (no usar)
            modelo = limpiar_texto(row.iloc[8]) if len(row) > 8 else ""  # presentacion (columna 8)
            marca = limpiar_texto(row.iloc[9]) if len(row) > 9 else ""   # laboratorio (columna 9)
            
            # Verificar si es una línea de categoría (contiene solo texto sin código numérico)
            if codigo and not re.match(r'^\d{6}', codigo) and ('CONVENIENCIA' in codigo or 'ACCESORIOS' in codigo):
                categoria_actual = codigo
                continue
            
            # Verificar si es un producto válido (tiene código numérico y nombre)
            if (codigo and re.match(r'^\d{9}', codigo) and 
                nombre and len(nombre) > 5 and 
                marca and marca != ""):
                
                # Limpiar el nombre del producto (medicamento)
                medicamento_limpio = nombre.strip()
                
                # El laboratorio es la marca
                laboratorio = marca if marca and marca != "" else "VARIOS"
                
                # La presentación es el modelo
                presentacion = modelo if modelo and modelo.strip() else f"Código: {codigo}"
                
                # Agregar a la lista de productos
                productos.append({
                    'codigo': codigo,
                    'nombre': medicamento_limpio,
                    'presentacion': presentacion,
                    'laboratorio': laboratorio,
                    'categoria': categoria_actual,
                    'precio': 0.0,  # Precio por defecto
                    'stock': 100    # Stock por defecto
                })
        
        print(f"\n✅ Se encontraron {len(productos)} productos válidos")
        
        # Conectar a la base de datos
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        
        # Limpiar tabla de inventario
        cursor.execute('DELETE FROM inventario')
        
        # Insertar productos en la base de datos
        for producto in productos:
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
        conn.close()
        
        print("✅ Inventario cargado exitosamente en la base de datos")
        
        # Mostrar estadísticas
        laboratorios = {}
        categorias = {}
        for producto in productos:
            lab = producto['laboratorio']
            cat = producto['categoria']
            laboratorios[lab] = laboratorios.get(lab, 0) + 1
            if cat:
                categorias[cat] = categorias.get(cat, 0) + 1
        
        estadisticas = {
            'total_productos': len(productos),
            'total_laboratorios': len(laboratorios),
            'total_categorias': len(categorias),
            'laboratorios': laboratorios,
            'categorias': categorias,
            'archivo_procesado': archivo_excel
        }
        
        print("\n📊 Estadísticas por laboratorio:")
        for lab, count in sorted(laboratorios.items(), key=lambda x: x[1], reverse=True):
            print(f"  {lab}: {count} productos")
        
        return True, estadisticas
        
    except Exception as e:
        print(f"❌ Error al procesar Excel: {e}")
        return False, f"Error: {str(e)}"

def backup_antes_de_procesar():
    """Crear backup antes de procesar el Excel"""
    try:
        # Crear carpeta backups si no existe
        if not os.path.exists('backups'):
            os.makedirs('backups')
        
        conn = sqlite3.connect('farmacia.db')
        
        # Crear backup con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/backup_antes_excel_{timestamp}.db"
        
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
    print("📊 Iniciando procesamiento de Excel original...")
    
    # Crear backup antes de procesar
    if backup_antes_de_procesar():
        # Procesar Excel
        success, result = procesar_excel_original('inventarioraw.xlsx')
        if success:
            print("\n✅ Procesamiento completado exitosamente")
            print(f"📊 Estadísticas: {result}")
        else:
            print(f"\n❌ Error en el procesamiento: {result}")
    else:
        print("❌ No se pudo crear el backup, abortando procesamiento") 