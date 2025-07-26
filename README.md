# Sistema de Gestión de Farmacia

Sistema web para gestión de inventario y ventas de farmacia.

## 🚀 Deploy Gratuito

### Opción 1: Railway (Recomendado)

1. **Crear cuenta en Railway**
   - Ve a [railway.app](https://railway.app)
   - Regístrate con GitHub

2. **Crear nuevo proyecto**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio


3. **Configurar base de datos**
   - En tu proyecto, click en "New"
   - Selecciona "Database" → "PostgreSQL"
   - Railway automáticamente configurará la variable `DATABASE_URL`

4. **Deploy automático**
   - Railway detectará automáticamente que es una app Python
   - El deploy comenzará automáticamente

### Opción 2: Render

1. **Crear cuenta en Render**
   - Ve a [render.com](https://render.com)
   - Regístrate con GitHub

2. **Crear nuevo Web Service**
   - Click en "New" → "Web Service"
   - Conecta tu repositorio
   - Configura:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Environment**: Python 3

3. **Configurar base de datos**
   - Click en "New" → "PostgreSQL"
   - Copia la URL de conexión
   - En tu Web Service, agrega variable de entorno:
     - **Key**: `DATABASE_URL`
     - **Value**: La URL de PostgreSQL

### Opción 3: Heroku

1. **Instalar Heroku CLI**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   ```

2. **Login y crear app**
   ```bash
   heroku login
   heroku create tu-farmacia-app
   ```

3. **Configurar base de datos**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Preparar para deploy"
   git push heroku main
   ```

## 📁 Estructura del Proyecto

```
SistemaFarmacia/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración para deploy
├── runtime.txt           # Versión de Python
├── templates/            # Plantillas HTML
│   ├── index.html
│   ├── inventario.html
│   └── historial.html
└── backups/              # Backups de base de datos
```

## 🔧 Variables de Entorno

- `DATABASE_URL`: URL de conexión a PostgreSQL (configurada automáticamente)
- `PORT`: Puerto de la aplicación (configurado automáticamente)

## 📊 Funcionalidades

- ✅ Gestión de inventario
- ✅ Registro de ventas
- ✅ Historial de transacciones
- ✅ Exportación a Excel
- ✅ Sincronización de inventario
- ✅ Búsqueda de productos
- ✅ Estadísticas en tiempo real

## 🌐 Acceso

Una vez desplegado, tu aplicación estará disponible en:
- **Railway**: `https://tu-app.railway.app`
- **Render**: `https://tu-app.onrender.com`
- **Heroku**: `https://tu-farmacia-app.herokuapp.com`

## 💡 Consejos

1. **Para 2 farmacias**: Railway es la mejor opción por su simplicidad
2. **Backup automático**: Los datos se guardan en PostgreSQL en la nube
3. **Acceso desde cualquier lugar**: Usa la URL desde cualquier dispositivo
4. **Sin mantenimiento**: Las plataformas manejan actualizaciones automáticamente

## 🆘 Soporte

Si tienes problemas con el deploy:
1. Verifica que todos los archivos estén en el repositorio
2. Revisa los logs de la plataforma
3. Asegúrate de que la base de datos esté configurada correctamente 