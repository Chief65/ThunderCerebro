$envLines = Get-Content (Join-Path $PSScriptRoot ".env")
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$channelId = "1552723526996336724"
$url = "https://discord.com/api/v10/channels/$channelId/messages"
$userAgent = "DiscordBot (https://thundermc.es, 1.0.0)"

$payloadPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot\menu_discord_thundermc_ready.json"
$img1 = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\campamento_dia\campamento_dia_1138x640.jpg"
$img2 = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\minecraft_compass_transparent.png"

Write-Host "Enviando embed mas reciente a canal $channelId..."
$curlOut = & curl.exe -s -X POST $url `
    -H "Authorization: Bot $token" `
    -H "User-Agent: $userAgent" `
    -F "files[0]=@$img1" `
    -F "files[1]=@$img2" `
    -F "payload_json=<$payloadPath;type=application/json"

$resObj = $curlOut | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($resObj.id) {
    Write-Host "SUCCESS: Mensaje enviado exitosamente."
    Write-Host "MESSAGE_ID: $($resObj.id)"
} else {
    Write-Error "ERROR: $curlOut"
    exit 1
}
