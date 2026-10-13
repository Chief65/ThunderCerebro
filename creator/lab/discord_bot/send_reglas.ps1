$envFile = Join-Path $PSScriptRoot ".env"
$envLines = Get-Content $envFile
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$channelId = ($envLines | Where-Object { $_ -match "^DISCORD_CHANNEL_ID=(.+)" } | ForEach-Object { $matches[1] }).Trim()

$payloadPath = Join-Path $PSScriptRoot "test_reglas_embed.json"
$url = "https://discord.com/api/v10/channels/$channelId/messages"
$userAgent = "DiscordBot (https://thundermc.es, 1.0.0)"

Write-Host "Enviando embed de reglas a Discord [$channelId]..."

$curlOut = & curl.exe -s -X POST $url `
    -H "Authorization: Bot $token" `
    -H "User-Agent: $userAgent" `
    -H "Content-Type: application/json; charset=utf-8" `
    --data-binary "@$payloadPath"

$resObj = $curlOut | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($resObj.id) {
    Write-Host "Mensaje de reglas enviado exitosamente!"
    Write-Host "ID del Mensaje: $($resObj.id)"
} else {
    Write-Error "Respuesta Discord: $curlOut"
}
