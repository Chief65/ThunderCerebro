$envPath = "creator/lab/discord_bot/.env"
$envLines = Get-Content $envPath
$token = ""
foreach ($line in $envLines) {
    $trimmed = $line.Trim()
    if ($trimmed.StartsWith("DISCORD_BOT_TOKEN=")) {
        $token = $trimmed.Substring("DISCORD_BOT_TOKEN=".Length).Trim()
    }
}

$headers = @{ "Authorization" = "Bot $token" }

try {
    $guilds = Invoke-RestMethod -Uri "https://discord.com/api/v10/users/@me/guilds" -Headers $headers
    foreach ($g in $guilds) {
        Write-Output "GUILD: $($g.name) ($($g.id))"
        $channels = Invoke-RestMethod -Uri "https://discord.com/api/v10/guilds/$($g.id)/channels" -Headers $headers
        foreach ($c in $channels) {
            if ($c.type -eq 0 -or $c.type -eq 5) {
                Write-Output "  - #$($c.name) ($($c.id))"
            }
        }
    }
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}
