param(
    [string]$Player = "SrRamos",
    [string]$Package = "Rango Titan (Permanente)"
)

$envFile = Join-Path $PSScriptRoot ".env"
$envLines = Get-Content $envFile
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$channelId = ($envLines | Where-Object { $_ -match "^DISCORD_CHANNEL_ID=(.+)" } | ForEach-Object { $matches[1] }).Trim()

$templateFile = Join-Path $PSScriptRoot "..\..\output\discord\tebex_purchase_embed.json"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$template = [System.IO.File]::ReadAllText($templateFile, $utf8NoBom)

# Simular compra de prueba con las variables dinámicas
$payloadText = $template `
    -replace '\{player\}', $Player `
    -replace '\{package\}', $Package

$url = "https://discord.com/api/v10/channels/$channelId/messages"
$userAgent = "DiscordBot (https://thundermc.es, 1.0.0)"

$tempPayload = Join-Path $PSScriptRoot "temp_purchase.json"
[System.IO.File]::WriteAllText($tempPayload, $payloadText, $utf8NoBom)

Write-Host "Enviando simulación de compra ($Player / $Package) a Discord [$channelId]..."

$curlOut = & curl.exe -s -X POST $url `
    -H "Authorization: Bot $token" `
    -H "User-Agent: $userAgent" `
    -H "Content-Type: application/json; charset=utf-8" `
    --data-binary "@$tempPayload"

Remove-Item $tempPayload -ErrorAction SilentlyContinue

$resObj = $curlOut | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($resObj.id) {
    Write-Host "Mensaje de compra enviado exitosamente!"
    Write-Host "ID del Mensaje: $($resObj.id)"
} else {
    Write-Error "Respuesta Discord: $curlOut"
}
