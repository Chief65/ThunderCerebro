param(
    [string]$PayloadFile = "menu_discord_thundermc.json",
    [string]$ImagePath = "",
    [string]$TargetChannel = ""
)

$envFile = Join-Path $PSScriptRoot ".env"
if (-not (Test-Path $envFile)) {
    Write-Error "No se encontro el archivo .env"
    exit 1
}

$envLines = Get-Content $envFile
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$defaultChannelId = ($envLines | Where-Object { $_ -match "^DISCORD_CHANNEL_ID=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$channelId = if ($TargetChannel) { $TargetChannel } else { $defaultChannelId }

$fullPayloadPath = if (Test-Path $PayloadFile) { $PayloadFile } else { Join-Path $PSScriptRoot $PayloadFile }
if (-not (Test-Path $fullPayloadPath)) {
    Write-Error "No se encontro el payload: $fullPayloadPath"
    exit 1
}

$payloadText = [System.IO.File]::ReadAllText($fullPayloadPath, [System.Text.Encoding]::UTF8)

if (-not $ImagePath) {
    if ($payloadText -match '"attachment://([^"]+)"') {
        $attachedFileName = $matches[1]
        $possiblePaths = @(
            (Join-Path $PSScriptRoot $attachedFileName),
            (Join-Path "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\campamento_dia" $attachedFileName),
            (Join-Path "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders" $attachedFileName)
        )
        foreach ($p in $possiblePaths) {
            if (Test-Path $p) {
                $ImagePath = $p
                break
            }
        }
    }
}

$url = "https://discord.com/api/v10/channels/$channelId/messages"
$userAgent = "DiscordBot (https://thundermc.es, 1.0.0)"

if ($ImagePath -and (Test-Path $ImagePath)) {
    Write-Host "Enviando $fullPayloadPath con adjunto [$ImagePath] a Discord [$channelId]..."
    
    # En curl, '<' lee el archivo directamente para payload_json sin problemas de escape
    $curlOut = & curl.exe -s -X POST $url `
        -H "Authorization: Bot $token" `
        -H "User-Agent: $userAgent" `
        -F "files[0]=@$ImagePath" `
        -F "payload_json=<$fullPayloadPath;type=application/json"
        
    $resObj = $curlOut | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($resObj.id) {
        Write-Host "Mensaje enviado exitosamente con adjunto!"
        Write-Host "ID del Mensaje: $($resObj.id)"
    } else {
        Write-Error "Respuesta Discord: $curlOut"
        exit 1
    }
} else {
    Write-Host "Enviando $fullPayloadPath a Discord [$channelId]..."
    $curlOut = & curl.exe -s -X POST $url `
        -H "Authorization: Bot $token" `
        -H "User-Agent: $userAgent" `
        -H "Content-Type: application/json; charset=utf-8" `
        -d "@$fullPayloadPath"
        
    $resObj = $curlOut | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($resObj.id) {
        Write-Host "Mensaje enviado exitosamente!"
        Write-Host "ID del Mensaje: $($resObj.id)"
    } else {
        Write-Error "Respuesta Discord: $curlOut"
        exit 1
    }
}
