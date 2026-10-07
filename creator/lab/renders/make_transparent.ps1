param(
    [string]$InputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_avatar\valyr_avatar_discord_1.jpg",
    [string]$OutputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_avatar\valyr_avatar_discord_transparent.png"
)

$csFile = Join-Path $PSScriptRoot "BackgroundRemover.cs"
$csCode = Get-Content $csFile -Raw

Add-Type -TypeDefinition $csCode -ReferencedAssemblies "System.Drawing"

Write-Host "Generando PNG transparente..."
[ThunderRender.BackgroundRemover]::CreateTransparentPng($InputPath, $OutputPath)

Get-Item $OutputPath | Select-Object FullName, Length
