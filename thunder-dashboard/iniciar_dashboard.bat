@echo off
title Thunder Telemetry Dashboard — Sr Ramos
cd /d "%~dp0"

echo ======================================================
echo   THUNDER CEREBRO — DASHBOARD DE TELEMETRIA Y MERCADO
echo ======================================================
echo.
echo Iniciando servidor local en http://localhost:3838 ...
echo.

:: Espera 1 segundo y abre el navegador por defecto
start "" http://localhost:3838

:: Inicia el servidor Node.js
node server.js

pause
