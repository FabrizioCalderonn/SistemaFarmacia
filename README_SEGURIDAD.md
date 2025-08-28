# 🔐 Guía de Seguridad - Sistema de Farmacia

## Contraseña de Administrador

El sistema ahora requiere una contraseña de administrador para eliminar registros. Esto es una medida de seguridad para prevenir eliminaciones accidentales o no autorizadas.

### Configuración de la Contraseña

#### Opción 1: Variable de Entorno (Recomendado para producción)

```bash
# En Windows (PowerShell)
$env:ADMIN_PASSWORD="tu_contraseña_segura_aqui"

# En Windows (CMD)
set ADMIN_PASSWORD=tu_contraseña_segura_aqui

# En Linux/Mac
export ADMIN_PASSWORD="tu_contraseña_segura_aqui"
```

#### Opción 2: Archivo .env (Desarrollo local)

Crear un archivo `.env` en la raíz del proyecto:

```env
ADMIN_PASSWORD=tu_contraseña_segura_aqui
SECRET_KEY=tu_clave_secreta_aqui
```

#### Opción 3: Modificar config.py (Solo para desarrollo)

Editar el archivo `config.py`:

```python
ADMIN_PASSWORD = 'tu_contraseña_segura_aqui'
```

### Contraseña por Defecto

⚠️ **ADVERTENCIA**: La contraseña por defecto es `admin123`. **DEBE CAMBIARSE** antes de usar en producción.

### Funcionalidades Protegidas

- ✅ **Eliminar registros de ventas/devoluciones**
- ✅ **Eliminar productos del inventario**
- ✅ **Operaciones críticas del sistema**

### Funcionalidades NO Protegidas

- ❌ **Crear registros**
- ❌ **Editar registros**
- ❌ **Ver historial**
- ❌ **Exportar datos**

### Mejores Prácticas de Seguridad

1. **Contraseña Fuerte**: Use al menos 12 caracteres con mayúsculas, minúsculas, números y símbolos
2. **No Compartir**: La contraseña solo debe ser conocida por administradores autorizados
3. **Rotación**: Cambie la contraseña periódicamente
4. **Variables de Entorno**: Use variables de entorno en lugar de hardcodear contraseñas
5. **Logs**: Revise regularmente los logs de eliminación

### Ejemplo de Contraseña Segura

```
F@rm4c14_2024_S3gur@
```

### Recuperación de Contraseña

Si olvida la contraseña de administrador:

1. Detenga la aplicación
2. Configure una nueva contraseña usando una de las opciones anteriores
3. Reinicie la aplicación

### Monitoreo de Actividad

El sistema registra todas las eliminaciones con:
- Timestamp de la operación
- ID del registro eliminado
- Usuario que realizó la operación (si está disponible)

### Configuración de Producción

Para entornos de producción, configure:

```bash
# Contraseña de administrador
ADMIN_PASSWORD=contraseña_muy_segura_aqui

# Clave secreta de Flask
SECRET_KEY=clave_secreta_muy_larga_y_compleja

# Cookies seguras (si usa HTTPS)
SESSION_COOKIE_SECURE=true

# Logging detallado
LOG_LEVEL=INFO
```

### Contacto de Soporte

Si tiene problemas con la configuración de seguridad, contacte al administrador del sistema.

---

**Nota**: Esta guía debe mantenerse actualizada con cualquier cambio en las políticas de seguridad del sistema.
