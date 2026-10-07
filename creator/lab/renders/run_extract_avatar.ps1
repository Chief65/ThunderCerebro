param(
    [string]$InputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_avatar\valyr_bot_pfp_v2.jpg",
    [string]$OutputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_avatar\valyr_bot_pfp_transparent.png"
)

$csFile = Join-Path $PSScriptRoot "ExtractAvatarPng.cs"
$csCode = Get-Content $csFile -Raw

Add-Type -TypeDefinition $csCode -ReferencedAssemblies "System.Drawing"

Write-Host "Extrayendo fondo y generando PNG transparente..."
[ThunderRender.AvatarPngExtractor]::Extract($InputPath, $OutputPath)

Get-Item $OutputPath | Select-Object FullName, Length
