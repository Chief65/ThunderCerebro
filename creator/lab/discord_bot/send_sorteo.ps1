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

$payloadJson = Get-Content "creator/lab/discord_bot/sorteo_embed.json" -Raw -Encoding utf8

$headers = @{
    "Authorization" = "Bot $token"
    "Content-Type"  = "application/json; charset=utf-8"
}

$url = "https://discord.com/api/v10/channels/$channelId/messages"

Write-Output "Enviando sorteo a canal $channelId..."
try {
    $res = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $payloadJson
    Write-Output "SUCCESS: Mensaje enviado con ID: $($res.id)"
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        Write-Output "DETAILS: $($reader.ReadToEnd())"
    }
}
