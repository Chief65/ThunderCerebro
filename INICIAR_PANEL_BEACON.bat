@echo off
chcp 65001 > nul
title BEACON // ThunderCerebro Control Center
color 0E

echo ===============================================================================
echo                ⚡ BEACON // THUNDER CEREBRO CONTROL CENTER ⚡
echo                       Panel de Control y Lanzador Antigravity
echo ===============================================================================
echo.
echo  [+] Verificando puerto 4848 y arrancando servidor local...

:: Verificar si el servidor ya esta escuchando activamente
netstat -ano | findstr /R /C:":4848 .*LISTENING" > nul
if %errorlevel% equ 0 (
    echo  [i] El servidor ya se encuentra activo en http://localhost:4848
) else (
    echo  [+] Iniciando backend PowerShell...
    start "BeaconServer" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0thunder-ai-control\server.ps1" -Port 4848
    
    :: Esperar hasta 6 segundos verificando activamente que el puerto este listo
    echo  [*] Esperando inicializacion del backend...
    for /L %%i in (1,1,12) do (
        ping 127.0.0.1 -n 2 > nul
        netstat -ano | findstr /R /C:":4848 .*LISTENING" > nul
        if not errorlevel 1 goto :server_ready
    )
)

:server_ready
echo.
echo  [+] Abriendo Panel de Control en modo aplicacion...

:: Intentar abrir con Edge en modo App nativo (sin barra de navegacion)
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app=http://localhost:4848 --window-size=1280,820
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --app=http://localhost:4848 --window-size=1280,820
) else (
    start http://localhost:4848
)

echo.
echo ===============================================================================
echo  Panel de Control iniciado correctamente en: http://localhost:4848
echo  Para cerrar el servidor, puede cerrar la ventana de PowerShell minimizada.
echo ===============================================================================
ping 127.0.0.1 -n 3 > nul
exit
