$envPath = "creator/lab/discord_bot/.env"
$envLines = Get-Content $envPath
$token = ""
$channelId = ""

foreach ($line in $envLines) {
    $trimmed = $line.Trim()
    if ($trimmed.StartsWith("DISCORD_BOT_TOKEN=")) {
        $token = $trimmed.Substring("DISCORD_BOT_TOKEN=".Length).Trim()
    }
    if ($trimmed.StartsWith("DISCORD_CHANNEL_ID=")) {
        $channelId = $trimmed.Substring("DISCORD_CHANNEL_ID=".Length).Trim()
    }
}

$jsonPath = (Resolve-Path "creator/lab/discord_bot/sorteo_embed.json").Path

Write-Output "Enviando sorteo a canal $channelId..."

$res = curl.exe -s -X POST `
    -H "Authorization: Bot $token" `
    -H "Content-Type: application/json; charset=utf-8" `
    -H "User-Agent: DiscordBot (ThunderMC, 1.0)" `
    --data-binary "@$jsonPath" `
    "https://discord.com/api/v10/channels/$channelId/messages"

$resJson = $res | ConvertFrom-Json
if ($resJson.id) {
    Write-Output "SUCCESS: Mensaje enviado con ID: $($resJson.id)"
} else {
    Write-Output "ERROR: $res"
}
