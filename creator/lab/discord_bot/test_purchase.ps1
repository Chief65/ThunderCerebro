param(
    [string]$Player = "SrRamos",
    [string]$Package = "Rango Titan (Permanente)"
)

$envFile = Join-Path $PSScriptRoot ".env"
$envLines = Get-Content $envFile
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$channelId = ($envLines | Where-Object { $_ -match "^DISCORD_CHANNEL_ID=(.+)" } | ForEach-Object { $matches[1] }).Trim()

$templateFile = Join-Path $PSScriptRoot "..\..\output\discord\tebex_purchase_embed.json"
$template = [System.IO.File]::ReadAllText($templateFile, [System.Text.Encoding]::UTF8)

# Simular compra de prueba con las variables dinámicas
$payloadText = $template `
    -replace '\{player\}', $Player `
    -replace '\{package\}', $Package

$imagePath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\campamento_dia\campamento_dia_1138x640.jpg"
$url = "https://discord.com/api/v10/channels/$channelId/messages"
$userAgent = "DiscordBot (https://thundermc.es, 1.0.0)"

$tempPayload = Join-Path $PSScriptRoot "temp_purchase.json"
[System.IO.File]::WriteAllText($tempPayload, $payloadText, [System.Text.Encoding]::UTF8)

Write-Host "Enviando simulación de compra ($Player / $Package) con imagen a Discord [$channelId]..."

$curlOut = & curl.exe -s -X POST $url `
    -H "Authorization: Bot $token" `
    -H "User-Agent: $userAgent" `
    -F "files[0]=@$imagePath" `
    -F "payload_json=<$tempPayload;type=application/json"

Remove-Item $tempPayload -ErrorAction SilentlyContinue

$resObj = $curlOut | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($resObj.id) {
    Write-Host "Mensaje de compra enviado exitosamente con adjunto!"
    Write-Host "ID del Mensaje: $($resObj.id)"
} else {
    Write-Error "Respuesta Discord: $curlOut"
}
