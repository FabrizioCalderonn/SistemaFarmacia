@echo off
echo ========================================
echo    Sistema de Farmacia - Iniciando
echo ========================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo 💡 Instala Python desde: https://python.org
    pause
    exit /b 1
)

REM Instalar dependencias si es necesario
echo 📦 Verificando dependencias...
pip install -r requirements.txt >nul 2>&1

REM Iniciar servidor en segundo plano
echo 🚀 Iniciando servidor...
start "" python app.py

REM Esperar un momento para que el servidor inicie
echo ⏳ Esperando que el servidor inicie...
timeout /t 3 /nobreak >nul

REM Abrir navegador
echo 🌐 Abriendo navegador...
start http://localhost:8081

echo.
echo ✅ Sistema iniciado correctamente!
echo 📍 URL: http://localhost:8081
echo.
echo 💡 Para detener el servidor, cierra la ventana de Python
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul 