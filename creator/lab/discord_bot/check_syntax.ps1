$lines = Get-Content "C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot\gateway_bot.ps1"
$depth = 0
for ($i = 0; $i -lt $lines.Length; $i++) {
    $line = $lines[$i]
    $opens = ([regex]::Matches($line, '\{')).Count
    $closes = ([regex]::Matches($line, '\}')).Count
    $depth = $depth + $opens - $closes
    if ($opens -gt 0 -or $closes -gt 0) {
        Write-Host ("Line " + ($i + 1) + ": (+" + $opens + " -" + $closes + ") Depth=" + $depth + " | " + $line.Trim())
    }
}
Write-Host ("Final Depth: " + $depth)
