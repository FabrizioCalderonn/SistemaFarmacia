import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

# Configuración de la aplicación
class Config:
    # Contraseña de administrador para eliminar registros
    # Cambiar esta contraseña en producción
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # Clave secreta para sesiones Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui_12345')
    
    # Configuración de farmacias
    FARMACIAS = {
        'farmacia1': {
            'nombre': 'Farmacia Popular',
            'direccion': 'Calle 15 de Septiembre Bo. San Pedro No. 3, Metapán, Santa Ana',
            'telefono': '2442-0202'
        },
        'farmacia2': {
            'nombre': 'Farmacia El Angel',
            'direccion': '2a. Calle Oriente, Av. Ignacio Gomez, Bo. San Pedro #3, Metapán, Santa Ana',
            'telefono': '2402-0110'
        }
    }
    
    # Farmacia por defecto
    FARMACIA_DEFAULT = 'farmacia1'
    
    # Configuración de base de datos
    DATABASE_TYPE = 'postgresql' if os.environ.get('DATABASE_URL') else 'sqlite'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE = 'farmacia.db'  # Solo para SQLite
    
    # Configuración de seguridad
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Configuración de archivos
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}
    
    # Configuración de backup
    BACKUP_DIR = 'backups'
    MAX_BACKUPS = 10  # Mantener solo los últimos 10 backups
