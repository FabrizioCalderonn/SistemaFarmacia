from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
from datetime import datetime
import tempfile
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
import werkzeug
import csv

# Importar psycopg2 para PostgreSQL o sqlite3 como fallback
try:
    import psycopg2
    import psycopg2.extras
    DATABASE_TYPE = 'postgresql'
except ImportError:
    import sqlite3
    DATABASE_TYPE = 'sqlite'

# Configuración de farmacias
FARMACIAS = {
    'farmacia1': {
        'nombre': 'Farmacia Principal',
        'direccion': 'Dirección 1',
        'telefono': 'Teléfono 1'
    },
    'farmacia2': {
        'nombre': 'Farmacia Sucursal',
        'direccion': 'Dirección 2', 
        'telefono': 'Teléfono 2'
    }
}

# Farmacia por defecto
FARMACIA_DEFAULT = 'farmacia1'

app = Flask(__name__)

# Configuración de la base de datos
if DATABASE_TYPE == 'postgresql':
    # Configuración para PostgreSQL (Supabase)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
else:
    # Configuración para SQLite (local)
    DATABASE = 'farmacia.db'

def get_db_connection():
    """Obtener conexión a la base de datos"""
    if DATABASE_TYPE == 'postgresql':
        if not DATABASE_URL:
            raise Exception("DATABASE_URL no configurada")
        try:
            # Configurar timeout y reintentos
            return psycopg2.connect(
                DATABASE_URL,
                connect_timeout=10,
                options='-c statement_timeout=30000'
            )
        except Exception as e:
            print(f"Error de conexión a PostgreSQL: {e}")
            raise
    else:
        return sqlite3.connect(DATABASE)

def init_db():
    """Inicializar la base de datos y crear solo tabla de registros"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if DATABASE_TYPE == 'postgresql':
        # Crear tabla de registros para PostgreSQL (inventario se lee desde CSV)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id SERIAL PRIMARY KEY,
                medicamento TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL DEFAULT 0.0,
                fecha TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL,
                observaciones TEXT,
                laboratorio TEXT NOT NULL,
                tipo_movimiento TEXT DEFAULT 'VENTA',
                fecha_vencimiento TEXT,
                lote TEXT,
                medico TEXT,
                junta_vigilancia TEXT,
                numero_inscripcion_clinica TEXT,
                farmacia TEXT DEFAULT 'farmacia1'
            )
        ''')
    else:
        # Crear tabla de registros para SQLite (inventario se lee desde CSV)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicamento TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL DEFAULT 0.0,
                fecha TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL,
                observaciones TEXT,
                laboratorio TEXT NOT NULL,
                tipo_movimiento TEXT DEFAULT 'VENTA',
                fecha_vencimiento TEXT,
                lote TEXT,
                medico TEXT,
                junta_vigilancia TEXT,
                numero_inscripcion_clinica TEXT,
                farmacia TEXT DEFAULT 'farmacia1'
            )
        ''')
    
    conn.commit()
    conn.close()

def load_inventory_from_csv():
    """Cargar inventario desde archivo CSV usando el script dedicado"""
    if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
        print("Archivo 'INVENTARIO PARA TRABAJO.csv' no encontrado")
        return
    
    print("Función load_inventory_from_csv deshabilitada - archivo procesar_inventario.py eliminado")

def sincronizar_inventario_web():
    """Sincronizar inventario desde la aplicación web"""
    try:
        # Importar y ejecutar el script de sincronización simplificado
        from sincronizar_inventario_simple import sincronizar_inventario
        success, result = sincronizar_inventario()
        return success, result
        
    except Exception as e:
        print(f"Error al sincronizar inventario: {e}")
        return False, f"Error: {str(e)}"

def procesar_excel_web(archivo):
    """Procesar archivo Excel desde la aplicación web"""
    try:
        # Importar y ejecutar el script de procesamiento de Excel simplificado
        from procesar_excel_simple import procesar_excel_original, backup_antes_de_procesar
        
        # Crear backup antes de procesar
        if not backup_antes_de_procesar():
            return False, "Error al crear backup"
        
        # Guardar archivo temporalmente
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"excel_upload_{timestamp}.xlsx"
        ruta_archivo = os.path.join(tempfile.gettempdir(), nombre_archivo)
        archivo.save(ruta_archivo)
        
        # Procesar el archivo
        success, result = procesar_excel_original(ruta_archivo)
        
        # Limpiar archivo temporal
        try:
            os.remove(ruta_archivo)
        except:
            pass
        
        return success, result
        
    except Exception as e:
        print(f"Error al procesar Excel: {e}")
        return False, f"Error: {str(e)}"

def get_laboratorios():
    """Obtener lista de laboratorios únicos desde CSV"""
    try:
        if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
            return []
        
        laboratorios = set()
        with open('INVENTARIO PARA TRABAJO.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('laboratorio'):
                    laboratorios.add(row['laboratorio'])
        
        return sorted(list(laboratorios))
    except Exception as e:
        print(f"Error al obtener laboratorios: {e}")
        return []

def get_medicamentos_by_laboratorio(laboratorio):
    """Obtener medicamentos por laboratorio desde CSV"""
    try:
        if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
            return []
        
        medicamentos = []
        with open('INVENTARIO PARA TRABAJO.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('laboratorio') == laboratorio:
                    medicamentos.append((
                        row.get('medicamento', ''),
                        row.get('presentacion', ''),
                        float(row.get('precio', 0)),
                        int(row.get('stock', 0))
                    ))
        
        return medicamentos
    except Exception as e:
        print(f"Error al obtener medicamentos: {e}")
        return []

def buscar_productos(termino):
    """Buscar productos por nombre o presentación desde CSV"""
    try:
        if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
            return []
        
        termino = termino.lower()
        productos = []
        with open('INVENTARIO PARA TRABAJO.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                medicamento = row.get('medicamento', '').lower()
                presentacion = row.get('presentacion', '').lower()
                
                if termino in medicamento or termino in presentacion:
                    productos.append({
                        'laboratorio': row.get('laboratorio', ''),
                        'medicamento': row.get('medicamento', ''),
                        'presentacion': row.get('presentacion', ''),
                        'precio': float(row.get('precio', 0)),
                        'stock': int(row.get('stock', 0))
                    })
        
        return productos
    except Exception as e:
        print(f"Error al buscar productos: {e}")
        return []

def get_estadisticas():
    """Obtener estadísticas del inventario desde CSV"""
    try:
        if not os.path.exists('INVENTARIO PARA TRABAJO.csv'):
            return {
                'total_productos': 0,
                'total_laboratorios': 0,
                'stock_bajo': 0,
                'sin_stock': 0
            }
        
        total_productos = 0
        laboratorios = set()
        stock_bajo = 0
        sin_stock = 0
        
        with open('INVENTARIO PARA TRABAJO.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_productos += 1
                if row.get('laboratorio'):
                    laboratorios.add(row['laboratorio'])
                
                stock = int(row.get('stock', 0))
                if stock == 0:
                    sin_stock += 1
                elif stock < 10:
                    stock_bajo += 1
        
        return {
            'total_productos': total_productos,
            'total_laboratorios': len(laboratorios),
            'stock_bajo': stock_bajo,
            'sin_stock': sin_stock
        }
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return {
            'total_productos': 0,
            'total_laboratorios': 0,
            'stock_bajo': 0,
            'sin_stock': 0
        }

def get_farmacia_actual():
    """Obtener la farmacia actual desde la sesión o parámetros"""
    farmacia = request.args.get('farmacia', FARMACIA_DEFAULT)
    if farmacia not in FARMACIAS:
        farmacia = FARMACIA_DEFAULT
    return farmacia

def get_farmacia_info(farmacia_id):
    """Obtener información de una farmacia específica"""
    return FARMACIAS.get(farmacia_id, FARMACIAS[FARMACIA_DEFAULT])

# Inicializar base de datos (solo para registros, no inventario)
init_db()

@app.route('/')
def index():
    """Página principal"""
    # Inicializar base de datos si es necesario
    initialize_database()
    
    laboratorios = get_laboratorios()
    estadisticas = get_estadisticas()
    return render_template('index.html', laboratorios=laboratorios, estadisticas=estadisticas)

@app.route('/api/laboratorios')
def api_laboratorios():
    """API para obtener lista de laboratorios"""
    laboratorios = get_laboratorios()
    return jsonify(laboratorios)

@app.route('/api/medicamentos/<laboratorio>')
def api_medicamentos(laboratorio):
    """API para obtener medicamentos por laboratorio"""
    medicamentos = get_medicamentos_by_laboratorio(laboratorio)
    return jsonify(medicamentos)

@app.route('/api/buscar')
def api_buscar():
    """API para buscar productos"""
    termino = request.args.get('q', '')
    if len(termino) < 2:
        return jsonify([])
    
    productos = buscar_productos(termino)
    return jsonify(productos)

@app.route('/guardar_registro', methods=['POST'])
def guardar_registro():
    """Guardar un nuevo registro"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['laboratorio', 'medicamento', 'cantidad', 'fecha']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Campo {field} es requerido'})
        
        # Insertar registro
        conn = get_db_connection()
        cursor = conn.cursor()
        
        farmacia_actual = get_farmacia_actual()
        
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                INSERT INTO registros (laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones, tipo_movimiento, 
                                     fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica, farmacia)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                data['laboratorio'],
                data['medicamento'],
                data['cantidad'],
                data['fecha'],
                datetime.now().isoformat(),
                data.get('observaciones', ''),
                data.get('tipo_movimiento', 'VENTA'),
                data.get('fecha_vencimiento', ''),
                data.get('lote', ''),
                data.get('medico', ''),
                data.get('junta_vigilancia', ''),
                data.get('numero_inscripcion_clinica', ''),
                farmacia_actual
            ))
            

        else:
            cursor.execute('''
                INSERT INTO registros (laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones, tipo_movimiento, 
                                 fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica, farmacia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['laboratorio'],
                data['medicamento'],
                data['cantidad'],
                data['fecha'],
                datetime.now().isoformat(),
                data.get('observaciones', ''),
                data.get('tipo_movimiento', 'VENTA'),
                data.get('fecha_vencimiento', ''),
                data.get('lote', ''),
                data.get('medico', ''),
                data.get('junta_vigilancia', ''),
                data.get('numero_inscripcion_clinica', ''),
                farmacia_actual
            ))
            

        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Registrado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/historial')
def historial():
    """Página de historial de registros"""
    return render_template('historial.html')

@app.route('/api/registros')
def api_registros():
    """API para obtener registros con filtros"""
    try:
        # Parámetros de filtro
        fecha_inicio = request.args.get('fecha_inicio', '')
        fecha_fin = request.args.get('fecha_fin', '')
        laboratorio = request.args.get('laboratorio', '')
        medicamento = request.args.get('medicamento', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Construir consulta con filtros
        query = '''
            SELECT id, laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones,
                   fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica
            FROM registros 
            WHERE 1=1
        '''
        params = []
        
        if fecha_inicio:
            query += ' AND fecha_ingreso >= %s'
            params.append(fecha_inicio + 'T00:00:00')
        
        if fecha_fin:
            query += ' AND fecha_ingreso <= %s'
            params.append(fecha_fin + 'T23:59:59')
        
        if laboratorio:
            query += ' AND laboratorio LIKE %s'
            params.append(f'%{laboratorio}%')
        
        if medicamento:
            query += ' AND medicamento LIKE %s'
            params.append(f'%{medicamento}%')
        
        query += ' ORDER BY fecha_ingreso DESC LIMIT 1000'
        
        cursor.execute(query, params)
        registros = cursor.fetchall()
        conn.close()
        
        # Formatear registros
        registros_formateados = []
        for reg in registros:
            registros_formateados.append({
                'id': reg[0],
                'laboratorio': reg[1],
                'medicamento': reg[2],
                'cantidad': reg[3],
                'fecha': reg[4],
                'fecha_ingreso': reg[5],
                'observaciones': reg[6],
                'fecha_vencimiento': reg[7] if len(reg) > 7 else '',
                'lote': reg[8] if len(reg) > 8 else '',
                'medico': reg[9] if len(reg) > 9 else '',
                'junta_vigilancia': reg[10] if len(reg) > 10 else '',
                'numero_inscripcion_clinica': reg[11] if len(reg) > 11 else ''
            })
        
        return jsonify(registros_formateados)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/registros/<int:registro_id>', methods=['PUT'])
def actualizar_registro(registro_id):
    """Actualizar un registro existente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['laboratorio', 'medicamento', 'cantidad', 'fecha']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Campo {field} es requerido'})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener el registro original para restaurar el stock
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('SELECT cantidad, laboratorio, medicamento FROM registros WHERE id = %s', (registro_id,))
        else:
            cursor.execute('SELECT cantidad, laboratorio, medicamento FROM registros WHERE id = ?', (registro_id,))
        registro_original = cursor.fetchone()
        
        if not registro_original:
            conn.close()
            return jsonify({'success': False, 'message': 'Registro no encontrado'})
        
        cantidad_original, laboratorio_original, medicamento_original = registro_original
        
        # Restaurar stock original
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                UPDATE inventario 
                SET stock = stock + %s 
                WHERE laboratorio = %s AND medicamento = %s
            ''', (cantidad_original, laboratorio_original, medicamento_original))
        else:
            cursor.execute('''
                UPDATE inventario 
                SET stock = stock + ? 
                WHERE laboratorio = ? AND medicamento = ?
            ''', (cantidad_original, laboratorio_original, medicamento_original))
        
        # Actualizar el registro
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                UPDATE registros 
                SET laboratorio = %s, medicamento = %s, cantidad = %s, fecha = %s, 
                    observaciones = %s, fecha_vencimiento = %s, lote = %s, medico = %s, junta_vigilancia = %s, numero_inscripcion_clinica = %s
                WHERE id = %s
            ''', (
                data['laboratorio'],
                data['medicamento'],
                data['cantidad'],
                data['fecha'],
                data.get('observaciones', ''),
                data.get('fecha_vencimiento', ''),
                data.get('lote', ''),
                data.get('medico', ''),
                data.get('junta_vigilancia', ''),
                data.get('numero_inscripcion_clinica', ''),
                registro_id
            ))
        else:
            cursor.execute('''
                UPDATE registros 
                SET laboratorio = ?, medicamento = ?, cantidad = ?, fecha = ?, 
                    observaciones = ?, fecha_vencimiento = ?, lote = ?, medico = ?, junta_vigilancia = ?, numero_inscripcion_clinica = ?
                WHERE id = ?
            ''', (
                data['laboratorio'],
                data['medicamento'],
                data['cantidad'],
                data['fecha'],
                data.get('observaciones', ''),
                data.get('fecha_vencimiento', ''),
                data.get('lote', ''),
                data.get('medico', ''),
                data.get('junta_vigilancia', ''),
                data.get('numero_inscripcion_clinica', ''),
                registro_id
            ))
        
        # Actualizar stock con la nueva cantidad
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                UPDATE inventario 
                SET stock = stock - %s 
                WHERE laboratorio = %s AND medicamento = %s
            ''', (data['cantidad'], data['laboratorio'], data['medicamento']))
        else:
            cursor.execute('''
                UPDATE inventario 
                SET stock = stock - ? 
                WHERE laboratorio = ? AND medicamento = ?
            ''', (data['cantidad'], data['laboratorio'], data['medicamento']))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Registro actualizado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/registros/<int:registro_id>', methods=['DELETE'])
def eliminar_registro(registro_id):
    """Eliminar un registro"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener información del registro antes de eliminarlo
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('SELECT cantidad, laboratorio, medicamento FROM registros WHERE id = %s', (registro_id,))
        else:
            cursor.execute('SELECT cantidad, laboratorio, medicamento FROM registros WHERE id = ?', (registro_id,))
        registro = cursor.fetchone()
        
        if not registro:
            conn.close()
            return jsonify({'success': False, 'message': 'Registro no encontrado'})
        
        cantidad, laboratorio, medicamento = registro
        
        # Restaurar stock al inventario
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                UPDATE inventario 
                SET stock = stock + %s 
                WHERE laboratorio = %s AND medicamento = %s
            ''', (cantidad, laboratorio, medicamento))
        else:
            cursor.execute('''
                UPDATE inventario 
                SET stock = stock + ? 
                WHERE laboratorio = ? AND medicamento = ?
            ''', (cantidad, laboratorio, medicamento))
        
        # Eliminar el registro
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('DELETE FROM registros WHERE id = %s', (registro_id,))
        else:
            cursor.execute('DELETE FROM registros WHERE id = ?', (registro_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Registro eliminado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/exportar_excel')
def exportar_excel():
    """Exportar registros a Excel"""
    try:
        # Obtener registros
        conn = get_db_connection()
        cursor = conn.cursor()
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                SELECT laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones,
                       fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica
                FROM registros 
                ORDER BY fecha_ingreso DESC
            ''')
        else:
            cursor.execute('''
                SELECT laboratorio, medicamento, cantidad, fecha, fecha_ingreso, observaciones,
                       fecha_vencimiento, lote, medico, junta_vigilancia, numero_inscripcion_clinica
                FROM registros 
                ORDER BY fecha_ingreso DESC
            ''')
        registros = cursor.fetchall()
        conn.close()
        
        # Crear archivo Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Registros de Farmacia"
        
        # Estilos
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        # Encabezados
        headers = ['Fecha Ingreso', 'Medicamento', 'Laboratorio', 'Cantidad', 'Fecha Compra', 'Fecha Vencimiento', 'Lote', 'Médico', 'Junta Vigilancia', 'Número Inscripción Clínica', 'Observaciones']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        
        # Datos
        for row, registro in enumerate(registros, 2):
            # Formatear fecha de ingreso para que sea más legible
            fecha_ingreso = registro[4]
            if fecha_ingreso:
                try:
                    fecha_obj = datetime.fromisoformat(fecha_ingreso.replace('Z', '+00:00'))
                    fecha_formateada = fecha_obj.strftime('%d/%m/%Y %H:%M:%S')
                except:
                    fecha_formateada = fecha_ingreso
            else:
                fecha_formateada = ''
            
            ws.cell(row=row, column=1, value=fecha_formateada)  # Fecha Ingreso
            ws.cell(row=row, column=2, value=registro[1])  # Medicamento
            ws.cell(row=row, column=3, value=registro[0])  # Laboratorio
            ws.cell(row=row, column=4, value=registro[2])  # Cantidad
            ws.cell(row=row, column=5, value=registro[3])  # Fecha Compra
            ws.cell(row=row, column=6, value=registro[6] if len(registro) > 6 else '')  # Fecha Vencimiento
            ws.cell(row=row, column=7, value=registro[7] if len(registro) > 7 else '')  # Lote
            ws.cell(row=row, column=8, value=registro[8] if len(registro) > 8 else '')  # Médico
            ws.cell(row=row, column=9, value=registro[9] if len(registro) > 9 else '')  # Junta Vigilancia
            ws.cell(row=row, column=10, value=registro[10] if len(registro) > 10 else '')  # Número Inscripción Clínica
            ws.cell(row=row, column=11, value=registro[5])  # Observaciones

        
        # Ajustar ancho de columnas
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Guardar archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"registros_farmacia_{timestamp}.xlsx"
        filepath = os.path.join(tempfile.gettempdir(), filename)
        wb.save(filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/inventario')
def inventario():
    """Página de inventario"""
    return render_template('inventario.html')

@app.route('/api/inventario')
def api_inventario():
    """API para obtener inventario con filtros"""
    try:
        laboratorio = request.args.get('laboratorio', '')
        stock_bajo = request.args.get('stock_bajo', 'false') == 'true'
        sin_stock = request.args.get('sin_stock', 'false') == 'true'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT laboratorio, medicamento, presentacion, precio, stock FROM inventario WHERE 1=1'
        params = []
        
        if laboratorio:
            query += ' AND laboratorio LIKE %s'
            params.append(f'%{laboratorio}%')
        
        if stock_bajo:
            query += ' AND stock < 10 AND stock > 0'
        
        if sin_stock:
            query += ' AND stock = 0'
        
        query += ' ORDER BY laboratorio, medicamento LIMIT 1000'
        
        cursor.execute(query, params)
        inventario = cursor.fetchall()
        conn.close()
        
        inventario_formateado = []
        for item in inventario:
            inventario_formateado.append({
                'laboratorio': item[0],
                'medicamento': item[1],
                'presentacion': item[2],
                'precio': item[3],
                'stock': item[4]
            })
        
        return jsonify(inventario_formateado)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/sincronizar_inventario', methods=['POST'])
def sincronizar_inventario_route():
    """Ruta para sincronizar inventario desde la web"""
    try:
        # Crear backup antes de sincronizar
        from sincronizar_inventario_simple import backup_registros
        if not backup_registros():
            return jsonify({'success': False, 'message': 'Error al crear backup'})
        
        # Realizar sincronización
        success, result = sincronizar_inventario_web()
        if success:
            return jsonify({
                'success': True, 
                'message': 'Inventario sincronizado exitosamente',
                'estadisticas': result
            })
        else:
            return jsonify({'success': False, 'message': result})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/eliminar_productos_obsoletos', methods=['POST'])
def eliminar_productos_obsoletos_route():
    """Ruta para eliminar productos obsoletos desde la web"""
    try:
        # Crear backup antes de eliminar
        from eliminar_productos_simple import backup_antes_de_eliminar
        if not backup_antes_de_eliminar():
            return jsonify({'success': False, 'message': 'Error al crear backup'})
        
        # Realizar eliminación
        from eliminar_productos_simple import eliminar_productos_obsoletos
        success, result = eliminar_productos_obsoletos()
        
        if success:
            if isinstance(result, dict):
                return jsonify({
                    'success': True, 
                    'message': 'Productos obsoletos eliminados exitosamente',
                    'estadisticas': result
                })
            else:
                return jsonify({
                    'success': True, 
                    'message': result
                })
        else:
            return jsonify({'success': False, 'message': result})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/cargar_excel', methods=['POST'])
def cargar_excel_route():
    """Ruta para cargar archivo Excel desde la web"""
    try:
        # Verificar si se envió un archivo
        if 'archivo' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        
        # Verificar si el archivo está vacío
        if archivo.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
        
        # Verificar extensión del archivo
        if not archivo.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'success': False, 'message': 'Solo se permiten archivos Excel (.xlsx, .xls)'})
        
        # Procesar el archivo Excel
        success, result = procesar_excel_web(archivo)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Archivo Excel procesado exitosamente',
                'estadisticas': result
            })
        else:
            return jsonify({'success': False, 'message': result})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/actualizar_inventario_csv', methods=['POST'])
def actualizar_inventario_csv():
    """Actualizar el archivo CSV de inventario desde la web"""
    try:
        # Verificar si se envió un archivo
        if 'archivo' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        
        # Verificar si el archivo está vacío
        if archivo.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
        
        # Verificar extensión del archivo
        if not archivo.filename.lower().endswith('.csv'):
            return jsonify({'success': False, 'message': 'Solo se permiten archivos CSV'})
        
        # Crear backup del CSV actual
        if os.path.exists('INVENTARIO PARA TRABAJO.csv'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"INVENTARIO PARA TRABAJO_backup_{timestamp}.csv"
            os.rename('INVENTARIO PARA TRABAJO.csv', backup_file)
        
        # Guardar el nuevo archivo
        archivo.save('INVENTARIO PARA TRABAJO.csv')
        
        return jsonify({
            'success': True, 
            'message': 'Inventario CSV actualizado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/cambiar_farmacia')
def cambiar_farmacia():
    """Página para cambiar de farmacia"""
    farmacias = FARMACIAS
    farmacia_actual = get_farmacia_actual()
    return render_template('cambiar_farmacia.html', farmacias=farmacias, farmacia_actual=farmacia_actual)

@app.route('/api/farmacias')
def api_farmacias():
    """API para obtener lista de farmacias"""
    return jsonify(FARMACIAS)

@app.route('/api/farmacia_actual')
def api_farmacia_actual():
    """API para obtener la farmacia actual"""
    farmacia_actual = get_farmacia_actual()
    return jsonify({
        'farmacia': farmacia_actual,
        'info': get_farmacia_info(farmacia_actual)
    })

# Para Vercel
app.debug = False

# Inicializar base de datos solo cuando sea necesario
def initialize_database():
    """Inicializar la base de datos solo cuando sea necesario"""
    try:
        init_db()
        print("Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False 