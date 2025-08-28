# 🚀 Instalación y Configuración de Seguridad

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
# Si tienes git
git clone <url-del-repositorio>
cd SistemaFarmacia

# O descargar y extraer manualmente
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

#### Opción A: Archivo .env (Recomendado para desarrollo)

```bash
# Copiar el archivo de ejemplo
cp env_example.txt .env

# Editar .env con tus valores
nano .env  # Linux/Mac
# o
notepad .env  # Windows
```

#### Opción B: Variables de entorno del sistema

```bash
# Windows (PowerShell)
$env:ADMIN_PASSWORD="tu_contraseña_segura"

# Windows (CMD)
set ADMIN_PASSWORD=tu_contraseña_segura

# Linux/Mac
export ADMIN_PASSWORD="tu_contraseña_segura"
```

### 4. Verificar la configuración

```bash
python test_seguridad.py
```

## Configuración de Seguridad

### Cambiar Contraseña por Defecto

⚠️ **IMPORTANTE**: La contraseña por defecto es `admin123`. DEBE CAMBIARSE.

#### Método 1: Variable de Entorno

```bash
export ADMIN_PASSWORD="F@rm4c14_2024_S3gur@"
```

#### Método 2: Archivo .env

```env
ADMIN_PASSWORD=F@rm4c14_2024_S3gur@
```

#### Método 3: Editar config.py (solo desarrollo)

```python
ADMIN_PASSWORD = 'F@rm4c14_2024_S3gur@'
```

### Generar Clave Secreta Segura

```python
import secrets
print(secrets.token_hex(32))
```

## Ejecutar la Aplicación

### Desarrollo Local

```bash
python app.py
```

### Con Variables de Entorno

```bash
# Windows
$env:ADMIN_PASSWORD="tu_contraseña"; python app.py

# Linux/Mac
ADMIN_PASSWORD="tu_contraseña" python app.py
```

## Verificar Funcionamiento

### 1. Acceder a la aplicación

Abrir navegador en: `http://localhost:5000`

### 2. Probar eliminación de registros

1. Ir a "Ver Historial"
2. Intentar eliminar un registro
3. Debe aparecer modal pidiendo contraseña

### 3. Ejecutar pruebas de seguridad

```bash
python test_seguridad.py
```

## Solución de Problemas

### Error: "No module named 'dotenv'"

```bash
pip install python-dotenv
```

### Error: "No module named 'requests'"

```bash
pip install requests
```

### La contraseña no funciona

1. Verificar que el archivo .env esté en la raíz del proyecto
2. Verificar que no haya espacios extra en la contraseña
3. Reiniciar la aplicación después de cambiar la configuración

### No aparece el modal de contraseña

1. Verificar que el JavaScript esté funcionando
2. Revisar la consola del navegador para errores
3. Verificar que el archivo historial.html esté actualizado

## Configuración de Producción

### 1. Usar variables de entorno del servidor

```bash
# No usar archivos .env en producción
export ADMIN_PASSWORD="contraseña_muy_segura_aqui"
export SECRET_KEY="clave_secreta_muy_larga_y_compleja"
```

### 2. Configurar HTTPS

```bash
export SESSION_COOKIE_SECURE=true
```

### 3. Configurar logging

```bash
export LOG_LEVEL=INFO
```

### 4. Usar servidor WSGI

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Estructura de Archivos

```
SistemaFarmacia/
├── app.py                 # Aplicación principal
├── config.py             # Configuración centralizada
├── requirements.txt      # Dependencias
├── .env                  # Variables de entorno (crear)
├── env_example.txt       # Ejemplo de variables
├── test_seguridad.py     # Pruebas de seguridad
├── README_SEGURIDAD.md   # Documentación de seguridad
└── INSTALACION_SEGURIDAD.md  # Este archivo
```

## Soporte

Si tienes problemas:

1. Revisar los logs de la aplicación
2. Ejecutar `python test_seguridad.py`
3. Verificar la configuración en `config.py`
4. Revisar la consola del navegador

## Notas de Seguridad

- ✅ Cambiar la contraseña por defecto
- ✅ Usar contraseñas fuertes (12+ caracteres)
- ✅ No compartir credenciales
- ✅ Revisar logs regularmente
- ✅ Mantener dependencias actualizadas
- ❌ No hardcodear contraseñas en el código
- ❌ No usar la contraseña por defecto en producción
