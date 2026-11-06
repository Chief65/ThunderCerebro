@echo off
chcp 65001 > nul
title THUNDERMC // Discord Gateway Bot & Postulaciones
color 0B

echo ===============================================================================
echo            ⚡ THUNDERMC // DISCORD BOT & SISTEMA DE POSTULACIONES ⚡
echo ===============================================================================
echo.
echo  [+] Iniciando Gateway en tiempo real con Python...
echo.

python -u "%~dp0creator\lab\discord_bot\gateway_bot.py"

pause
