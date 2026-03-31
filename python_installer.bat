@echo off
setlocal
title Instalador de Python 3.12

:: 1. Verificar permisos de Administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Ejecutando con permisos de Administrador.
) else (
    echo [!] ERROR: Por favor, haz clic derecho y selecciona "Ejecutar como administrador".
    pause
    exit /b 1
)

echo -----------------------------------------------------
echo  Instalando Python 3.12.9 (Version Estable para Audio)
echo -----------------------------------------------------

:: 2. Definir URL y Ruta temporal
set "PY_URL=https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe"
set "PY_EXE=%TEMP%\python_installer.exe"

:: 3. Descargar usando PowerShell (Nativo en Windows)
echo [1/3] Descargando instalador oficial...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('%PY_URL%', '%PY_EXE%')"

if not exist "%PY_EXE%" (
    echo [!] Error en la descarga. Comprueba tu conexion a internet.
    pause
    exit /b 1
)

:: 4. Ejecutar instalacion silenciosa
:: InstallAllUsers=1: Instala en C:\Program Files\Python312
:: PrependPath=1: Agrega Python a las variables de entorno (PATH)
echo [2/3] Instalando silenciosamente... Por favor espera.
start /wait "" "%PY_EXE%" /passive InstallAllUsers=1 PrependPath=1 Include_test=0

:: 5. Limpieza
echo [3/3] Finalizando...
del "%PY_EXE%"

echo -----------------------------------------------------
echo ✅ INSTALACION COMPLETADA
echo -----------------------------------------------------
echo IMPORTANTE: Debes CERRAR todas las ventanas de comandos 
echo actuales para que Windows reconozca el nuevo Python.
echo -----------------------------------------------------
pause