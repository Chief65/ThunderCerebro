param(
    [string]$InputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\menu_principal_taberna\menu_principal_taberna_9.jpg",
    [string]$OutputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\menu_principal_taberna\menu_principal_taberna_1138x640.jpg",
    [float]$Contrast = 1.08,
    [float]$Sharpness = 0.75
)

$csFile = Join-Path $PSScriptRoot "DiscordOptimizer.cs"
$csCode = Get-Content $csFile -Raw

Add-Type -TypeDefinition $csCode -ReferencedAssemblies "System.Drawing"

Write-Host "Generando activo nativo Discord 1138x640 con realce de contraste y micro-nitidez..."
[ThunderRender.DiscordOptimizer]::Optimize($InputPath, $OutputPath, $Contrast, $Sharpness)

Get-Item $OutputPath | Select-Object FullName, Length
