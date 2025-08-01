#!/usr/bin/env python3
"""
Módulo simple para manejar inventario en memoria
"""
import os

# Inventario en memoria (se carga al iniciar)
INVENTARIO_MEMORIA = []

def analizar_formato_linea():
    """Analizar el formato exacto de las líneas del archivo"""
    try:
        csv_path = 'INVENTARIO PARA TRABAJO.csv'
        if not os.path.exists(csv_path):
            return {"error": "Archivo no encontrado"}
        
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        
        header_found = False
        analisis = {
            'lineas_analizadas': [],
            'formato_detectado': None
        }
        
        for i, line in enumerate(lines[:10]):  # Solo las primeras 10 líneas
            line_original = line.strip()
            
            if 'Codigo' in line_original and 'Nombre' in line_original:
                header_found = True
                analisis['linea_encabezados'] = {
                    'numero': i + 1,
                    'contenido': line_original,
                    'partes_tab': line_original.split('\t'),
                    'partes_comas': line_original.split(',')
                }
                continue
            
            if header_found and line_original and not line_original.startswith('"Listado') and not line_original.startswith('"Reportes'):
                # Analizar línea de producto
                linea_analisis = {
                    'numero': i + 1,
                    'contenido_original': line_original,
                    'partes_tab': line_original.split('\t'),
                    'partes_comas': line_original.split(','),
                    'longitud_tab': len(line_original.split('\t')),
                    'longitud_comas': len(line_original.split(','))
                }
                
                # Limpiar comillas y analizar
                line_clean = line_original.replace('"', '')
                linea_analisis['contenido_limpio'] = line_clean
                linea_analisis['partes_tab_limpias'] = line_clean.split('\t')
                linea_analisis['partes_comas_limpias'] = line_clean.split(',')
                
                analisis['lineas_analizadas'].append(linea_analisis)
                
                if len(analisis['lineas_analizadas']) >= 3:
                    break
        
        return analisis
        
    except Exception as e:
        return {"error": str(e)}

def cargar_inventario():
    """Cargar inventario a memoria"""
    global INVENTARIO_MEMORIA
    INVENTARIO_MEMORIA = []
    
    try:
        csv_path = 'INVENTARIO PARA TRABAJO.csv'
        if not os.path.exists(csv_path):
            return False
        
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        
        header_found = False
        for line in lines:
            line = line.strip()
            
            if 'Codigo' in line and 'Nombre' in line:
                header_found = True
                continue
            
            if header_found and line and not line.startswith('"Listado') and not line.startswith('"Reportes'):
                # Usar CSV reader para manejar comillas correctamente
                import csv
                from io import StringIO
                
                # Crear un StringIO con la línea para usar csv.reader
                line_io = StringIO(line)
                reader = csv.reader(line_io)
                
                try:
                    parts = next(reader)  # Leer la línea como CSV
                    
                    if len(parts) >= 4:  # Código, Nombre, Modelo, Laboratorio
                        codigo = parts[0].strip()
                        nombre = parts[1].strip()
                        modelo = parts[2].strip()
                        laboratorio = parts[3].strip()
                        
                        # Solo agregar si tiene código y nombre válidos
                        if codigo and nombre and len(codigo) > 3 and len(nombre) > 3:
                            producto = {
                                'codigo': codigo,
                                'nombre': nombre,
                                'modelo': modelo,
                                'laboratorio': laboratorio,
                                'precio': 0.0,
                                'stock': 1
                            }
                            INVENTARIO_MEMORIA.append(producto)
                            
                            # Debug: mostrar los primeros productos
                            if len(INVENTARIO_MEMORIA) <= 3:
                                print(f"Producto cargado: {producto['nombre'][:30]}... -> Lab: {producto['laboratorio']}")
                except Exception as e:
                    print(f"Error procesando línea: {e}")
                    continue
        
        print(f"Inventario cargado: {len(INVENTARIO_MEMORIA)} productos")
        return True
        
    except Exception as e:
        print(f"Error al cargar inventario: {e}")
        return False

def get_laboratorios():
    """Obtener lista de laboratorios únicos"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    laboratorios = set()
    print(f"Analizando {len(INVENTARIO_MEMORIA)} productos para laboratorios...")
    
    for i, producto in enumerate(INVENTARIO_MEMORIA):
        if producto['laboratorio'] and producto['laboratorio'] != 'Sin especificar':
            # Normalizar el nombre del laboratorio
            lab_normalizado = producto['laboratorio'].strip()
            laboratorios.add(lab_normalizado)
            if i < 5:  # Mostrar los primeros 5 para debug
                print(f"Producto {i+1}: {producto['nombre'][:30]}... -> Laboratorio: '{producto['laboratorio']}'")
    
    laboratorios_lista = sorted(list(laboratorios))
    print(f"Laboratorios encontrados: {laboratorios_lista}")
    
    # Debug: mostrar laboratorios que contengan "med" o "pharma"
    laboratorios_med_pharma = [lab for lab in laboratorios_lista if 'med' in lab.lower() or 'pharma' in lab.lower()]
    if laboratorios_med_pharma:
        print(f"Laboratorios con 'med' o 'pharma': {laboratorios_med_pharma}")
    
    return laboratorios_lista

def get_medicamentos_by_laboratorio(laboratorio):
    """Obtener medicamentos por laboratorio"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    medicamentos = []
    print(f"Buscando medicamentos para laboratorio: '{laboratorio}'")
    print(f"Total productos en memoria: {len(INVENTARIO_MEMORIA)}")
    
    # Normalizar el laboratorio buscado
    laboratorio_buscar = laboratorio.lower().strip()
    
    for i, producto in enumerate(INVENTARIO_MEMORIA):
        # Normalizar el laboratorio del producto
        laboratorio_producto = producto['laboratorio'].lower().strip()
        
        # Comparación más flexible
        if laboratorio_producto == laboratorio_buscar or laboratorio_producto.startswith(laboratorio_buscar):
            medicamentos.append((
                producto['nombre'],
                producto['modelo'],
                producto['precio'],
                producto['stock']
            ))
            if len(medicamentos) <= 3:  # Debug: mostrar los primeros
                print(f"Medicamento encontrado: {producto['nombre'][:30]}... -> Lab: {producto['laboratorio']}")
    
    print(f"Total medicamentos encontrados para '{laboratorio}': {len(medicamentos)}")
    
    # Si no se encontraron medicamentos, mostrar algunos laboratorios disponibles para debug
    if len(medicamentos) == 0:
        print("No se encontraron medicamentos. Laboratorios disponibles:")
        laboratorios_disponibles = set()
        for producto in INVENTARIO_MEMORIA:
            if producto['laboratorio']:
                laboratorios_disponibles.add(producto['laboratorio'])
        
        for lab in sorted(laboratorios_disponibles):
            if 'med' in lab.lower() or 'pharma' in lab.lower():
                print(f"  - '{lab}' (similar a '{laboratorio}')")
    
    return medicamentos

def buscar_productos(termino):
    """Buscar productos por nombre"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    termino = termino.lower()
    productos = []
    print(f"Buscando productos con término: '{termino}'")
    print(f"Total productos en memoria: {len(INVENTARIO_MEMORIA)}")
    
    for i, producto in enumerate(INVENTARIO_MEMORIA):
        nombre = producto['nombre'].lower()
        if termino in nombre:
            productos.append({
                'laboratorio': producto['laboratorio'],
                'medicamento': producto['nombre'],
                'presentacion': producto['modelo'],
                'precio': producto['precio'],
                'stock': producto['stock']
            })
            if len(productos) <= 3:  # Debug: mostrar los primeros
                print(f"Producto encontrado: {producto['nombre'][:30]}...")
    
    print(f"Total productos encontrados con '{termino}': {len(productos)}")
    return productos

def debug_inventario():
    """Función de debug para mostrar información del inventario"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    debug_info = {
        'total_productos': len(INVENTARIO_MEMORIA),
        'primeros_productos': [],
        'laboratorios_unicos': set(),
        'laboratorios_conteo': {}
    }
    
    for i, producto in enumerate(INVENTARIO_MEMORIA):
        # Contar laboratorios
        lab = producto['laboratorio']
        if lab and lab != 'Sin especificar':
            debug_info['laboratorios_unicos'].add(lab)
            debug_info['laboratorios_conteo'][lab] = debug_info['laboratorios_conteo'].get(lab, 0) + 1
        
        # Mostrar primeros productos
        if i < 5:
            debug_info['primeros_productos'].append({
                'codigo': producto['codigo'],
                'nombre': producto['nombre'][:50],
                'laboratorio': producto['laboratorio']
            })
    
    debug_info['laboratorios_unicos'] = sorted(list(debug_info['laboratorios_unicos']))
    
    return debug_info

def get_estadisticas():
    """Obtener estadísticas del inventario"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    laboratorios = set()
    for producto in INVENTARIO_MEMORIA:
        if producto['laboratorio'] and producto['laboratorio'] != 'Sin especificar':
            laboratorios.add(producto['laboratorio'])
    
    return {
        'total_productos': len(INVENTARIO_MEMORIA),
        'total_laboratorios': len(laboratorios),
        'stock_bajo': 0,
        'sin_stock': 0
    } 