#!/usr/bin/env python3
"""
Módulo simple para manejar inventario en memoria
"""
import os

# Inventario en memoria (se carga al iniciar)
INVENTARIO_MEMORIA = []

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
                line = line.replace('"', '')
                parts = [part.strip() for part in line.split('\t') if part.strip()]
                
                if len(parts) >= 3:
                    codigo = parts[0]
                    nombre = parts[1]
                    modelo_marca = parts[2]
                    
                    if ',' in modelo_marca:
                        modelo, laboratorio = modelo_marca.rsplit(',', 1)
                        modelo = modelo.strip()
                        laboratorio = laboratorio.strip()
                    else:
                        modelo = modelo_marca.strip()
                        laboratorio = 'Sin especificar'
                    
                    if codigo and nombre and len(codigo.strip()) > 3 and len(nombre.strip()) > 3:
                        producto = {
                            'codigo': codigo.strip(),
                            'nombre': nombre.strip(),
                            'modelo': modelo,
                            'laboratorio': laboratorio,
                            'precio': 0.0,
                            'stock': 1
                        }
                        INVENTARIO_MEMORIA.append(producto)
                        
                        # Debug: mostrar los primeros productos
                        if len(INVENTARIO_MEMORIA) <= 3:
                            print(f"Producto cargado: {producto['nombre'][:30]}... -> Lab: {producto['laboratorio']}")
        
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
            laboratorios.add(producto['laboratorio'])
            if i < 5:  # Mostrar los primeros 5 para debug
                print(f"Producto {i+1}: {producto['nombre'][:30]}... -> Laboratorio: {producto['laboratorio']}")
    
    print(f"Laboratorios encontrados: {sorted(list(laboratorios))}")
    return sorted(list(laboratorios))

def get_medicamentos_by_laboratorio(laboratorio):
    """Obtener medicamentos por laboratorio"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    medicamentos = []
    for producto in INVENTARIO_MEMORIA:
        if producto['laboratorio'] == laboratorio:
            medicamentos.append((
                producto['nombre'],
                producto['modelo'],
                producto['precio'],
                producto['stock']
            ))
    
    return medicamentos

def buscar_productos(termino):
    """Buscar productos por nombre"""
    if not INVENTARIO_MEMORIA:
        cargar_inventario()
    
    termino = termino.lower()
    productos = []
    for producto in INVENTARIO_MEMORIA:
        nombre = producto['nombre'].lower()
        if termino in nombre:
            productos.append({
                'laboratorio': producto['laboratorio'],
                'medicamento': producto['nombre'],
                'presentacion': producto['modelo'],
                'precio': producto['precio'],
                'stock': producto['stock']
            })
    
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