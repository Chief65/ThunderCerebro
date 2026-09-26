@echo off
title ThunderMC Tebex Preview Server
cd /d "%~dp0"
echo Iniciando servidor de preview en http://localhost:3000...
node server.js
pause
