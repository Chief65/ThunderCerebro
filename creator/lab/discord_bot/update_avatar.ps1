$ErrorActionPreference = "Stop"

$envFile = Join-Path $PSScriptRoot ".env"
if (-not (Test-Path $envFile)) {
    Write-Error "No se encontro el archivo .env en $envFile"
    exit 1
}

$envLines = Get-Content $envFile
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()

$imagePath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_avatar\valyr_bot_pfp_zoom_neutral_transparent.png"
if (-not (Test-Path $imagePath)) {
    Write-Error "No se encontro la imagen en $imagePath"
    exit 1
}

Write-Host "Cargando imagen: $imagePath"
$bytes = [System.IO.File]::ReadAllBytes($imagePath)
$base64 = [System.Convert]::ToBase64String($bytes)
$dataUri = "data:image/png;base64,$base64"

$payload = @{
    avatar = $dataUri
} | ConvertTo-Json -Compress

$url = "https://discord.com/api/v10/users/@me"
$headers = @{
    "Authorization" = "Bot $token"
    "User-Agent"    = "DiscordBot (https://thundermc.es, 1.0.0)"
    "Content-Type"  = "application/json; charset=utf-8"
}

Write-Host "Enviando solicitud PATCH a Discord API ($url)..."
try {
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Patch -Body $payload
    Write-Host "Foto de perfil actualizada exitosamente!"
    Write-Host "Bot ID: $($response.id)"
    Write-Host "Usuario: $($response.username)"
    Write-Host "Nuevo Avatar Hash: $($response.avatar)"
    Write-Host "URL Avatar: https://cdn.discordapp.com/avatars/$($response.id)/$($response.avatar).png?size=1024"
} catch {
    Write-Error "Error al actualizar avatar en Discord: $_"
    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $errBody = $reader.ReadToEnd()
        Write-Error "Detalle de error API: $errBody"
    }
    exit 1
}
