# 🏥 Sistema de Farmacia - Deploy y Configuración Multi-Farmacia

## 🚀 Deploy en Render (Gratuito)

### 1. Preparar el repositorio
```bash
# Subir código a GitHub
git add .
git commit -m "Sistema multi-farmacia listo"
git push origin main
```

### 2. Configurar en Render
1. Ir a [render.com](https://render.com)
2. Crear cuenta con GitHub
3. Crear **Web Service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Crear **PostgreSQL Database**
5. Configurar variable de entorno: `DATABASE_URL`

### 3. Configurar farmacias
Editar `app.py` y modificar la sección `FARMACIAS`:

```python
FARMACIAS = {
    'farmacia1': {
        'nombre': 'Farmacia Principal',
        'direccion': 'Av. Principal 123',
        'telefono': '555-1234'
    },
    'farmacia2': {
        'nombre': 'Farmacia Sucursal',
        'direccion': 'Calle Secundaria 456',
        'telefono': '555-5678'
    }
}
```

## 📱 Uso del Sistema

### URLs para cada farmacia:
- **Farmacia Principal**: `https://tu-app.onrender.com/?farmacia=farmacia1`
- **Farmacia Sucursal**: `https://tu-app.onrender.com/?farmacia=farmacia2`
- **Selector de farmacia**: `https://tu-app.onrender.com/cambiar_farmacia`

### Funcionalidades:
✅ **Inventario compartido** - Mismo CSV para todas las farmacias
✅ **Registros separados** - Cada farmacia tiene sus propios registros
✅ **Estadísticas por farmacia** - Filtros automáticos
✅ **Exportación por farmacia** - Excel separado por farmacia

## 🔄 Actualizaciones del Sistema

### Desde cualquier lugar:
1. **Editar código** en GitHub (desde web o móvil)
2. **Push automático** - Render se actualiza automáticamente
3. **Sin interrupciones** - La aplicación sigue funcionando

### Actualizar inventario:
1. **Subir nuevo CSV** desde la web
2. **O editar directamente** en GitHub
3. **Cambios inmediatos** para todas las farmacias

## 💾 Gestión de Datos

### Inventario (CSV):
- Archivo: `INVENTARIO PARA TRABAJO.csv`
- Ubicación: Raíz del proyecto
- Compartido: Todas las farmacias
- Actualización: Subir nuevo archivo

### Registros (Base de datos):
- Tabla: `registros`
- Separación: Campo `farmacia`
- Backup: Automático en Render
- Exportación: Por farmacia

## 🔧 Configuración Avanzada

### Agregar nueva farmacia:
1. Editar `FARMACIAS` en `app.py`
2. Hacer commit y push
3. La nueva farmacia estará disponible inmediatamente

### Personalizar interfaz:
1. Editar templates en `templates/`
2. Modificar estilos CSS
3. Push para aplicar cambios

## 📊 Monitoreo

### Logs en Render:
- Dashboard de Render → Tu app → Logs
- Ver errores y actividad en tiempo real

### Estadísticas:
- Total de registros por farmacia
- Productos más vendidos
- Stock bajo y sin stock

## 🆘 Solución de Problemas

### Error de conexión:
- Verificar `DATABASE_URL` en Render
- Revisar logs en el dashboard

### CSV no se carga:
- Verificar formato del archivo
- Comprobar encoding UTF-8
- Revisar permisos de archivo

### Farmacia no aparece:
- Verificar configuración en `FARMACIAS`
- Limpiar cache del navegador
- Verificar parámetro `?farmacia=`

## 💡 Consejos

1. **Backup regular** del CSV de inventario
2. **Usar nombres descriptivos** para las farmacias
3. **Revisar logs** periódicamente
4. **Probar cambios** en desarrollo antes de subir

## 🎯 Ventajas de esta implementación:

✅ **Completamente gratuito** - Render + GitHub
✅ **Multi-farmacia** - Una sola aplicación
✅ **Actualizaciones remotas** - Desde cualquier lugar
✅ **Datos separados** - Cada farmacia independiente
✅ **Inventario compartido** - Fácil mantenimiento
✅ **Backup automático** - Sin pérdida de datos
✅ **Escalable** - Fácil agregar más farmacias

---

**¿Necesitas ayuda?** Revisa los logs en Render o contacta al desarrollador. 