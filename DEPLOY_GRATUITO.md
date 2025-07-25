# 🆓 Deploy 100% Gratuito - Supabase + Vercel

## 🎯 **Ventajas de esta combinación:**
✅ **Completamente gratuito** - Sin límites de tiempo
✅ **PostgreSQL sin expiración** - Base de datos permanente
✅ **Deploy automático** - Desde GitHub
✅ **Muy rápido** - CDN global
✅ **Sin configuración compleja** - Setup en 10 minutos

---

## 🚀 **Paso 1: Configurar Supabase (Base de datos)**

### 1. Crear cuenta en Supabase
1. Ir a [supabase.com](https://supabase.com)
2. Crear cuenta con GitHub
3. Crear nuevo proyecto

### 2. Obtener credenciales
1. En el dashboard de Supabase → Settings → Database
2. Copiar:
   - **Database URL**
   - **Database Password**

### 3. Configurar base de datos
```sql
-- Ejecutar en SQL Editor de Supabase
CREATE TABLE registros (
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
);
```

---

## 🚀 **Paso 2: Configurar Vercel (Hosting)**

### 1. Crear cuenta en Vercel
1. Ir a [vercel.com](https://vercel.com)
2. Crear cuenta con GitHub
3. Importar tu repositorio

### 2. Configurar variables de entorno
En Vercel → Tu proyecto → Settings → Environment Variables:
- **Key**: `DATABASE_URL`
- **Value**: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`

### 3. Deploy automático
- Vercel detectará automáticamente que es Flask
- Deploy en 2-3 minutos
- URL: `https://tu-app.vercel.app`

---

## 🚀 **Paso 3: Configurar el código**

### 1. Actualizar requirements.txt
```txt
Flask==3.0.0
openpyxl==3.1.2
Werkzeug==3.0.1
psycopg2-binary==2.9.9
xlrd==2.0.1
```

### 2. Crear vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 3. Modificar app.py (solo la conexión)
```python
# Configuración de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
```

---

## 📱 **Uso del Sistema**

### URLs:
- **Farmacia 1**: `https://tu-app.vercel.app/?farmacia=farmacia1`
- **Farmacia 2**: `https://tu-app.vercel.app/?farmacia=farmacia2`
- **Selector**: `https://tu-app.vercel.app/cambiar_farmacia`

### Funcionalidades:
✅ **Inventario compartido** - CSV en el repositorio
✅ **Registros separados** - Por farmacia en Supabase
✅ **Actualizaciones remotas** - Push a GitHub
✅ **Backup automático** - Supabase hace backup diario

---

## 🔄 **Actualizaciones**

### Desde cualquier lugar:
1. **Editar en GitHub** (web/móvil)
2. **Push automático** - Vercel se actualiza
3. **Sin interrupciones** - Deploy en segundos

### Actualizar inventario:
1. **Subir CSV** desde la web
2. **O editar** directamente en GitHub
3. **Cambios inmediatos**

---

## 💰 **Costos: $0 USD/mes**

### Supabase (Gratuito):
- 500MB base de datos
- 50,000 filas/mes
- 2GB transferencia
- **Sin expiración**

### Vercel (Gratuito):
- Deploy ilimitado
- 100GB transferencia
- **Sin expiración**

---

## 🆚 **Comparación con Render:**

| Característica | Render | Supabase + Vercel |
|----------------|--------|-------------------|
| **Costo** | $5/mes después de 30 días | $0/mes siempre |
| **Base de datos** | Expira en 30 días | Sin expiración |
| **Velocidad** | Buena | Excelente (CDN) |
| **Deploy** | Automático | Automático |
| **Backup** | Manual | Automático |

---

## 🎯 **Ventajas adicionales:**

✅ **Dashboard web** - Gestionar datos desde Supabase
✅ **APIs automáticas** - Supabase genera APIs
✅ **Autenticación** - Sistema de usuarios incluido
✅ **Real-time** - Actualizaciones en tiempo real
✅ **Escalable** - Fácil migrar a planes pagos

---

## 🚀 **Deploy en 10 minutos:**

1. **Crear Supabase** (2 min)
2. **Configurar Vercel** (3 min)
3. **Subir código** (2 min)
4. **Probar sistema** (3 min)

**¿Listo para empezar?** Te ayudo con cada paso. 