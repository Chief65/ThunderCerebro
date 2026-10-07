param(
    [string]$InputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\menu_principal_taberna\menu_principal_taberna_9.jpg",
    [string]$OutputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\menu_principal_taberna\menu_principal_taberna_9_4k.jpg",
    [float]$Sharpness = 0.8
)

$csFile = Join-Path $PSScriptRoot "Enhancer.cs"
$csCode = Get-Content $csFile -Raw

Add-Type -TypeDefinition $csCode -ReferencedAssemblies "System.Drawing"

Write-Host "Procesando imagen con Unsharp Masking 4K UHD..."
[ThunderRender.Enhancer]::Process($InputPath, $OutputPath, 3840, 2160, $Sharpness)
Write-Host "Generado en: $OutputPath"

# Medicion de nitidez
$bmp = [System.Drawing.Bitmap]::FromFile($OutputPath)
$w = $bmp.Width; $h = $bmp.Height
$diffSum = 0; $count = 0
for ($y = 200; $y -lt 800; $y += 2) {
    for ($x = 200; $x -lt 800; $x += 2) {
        $c1 = $bmp.GetPixel($x, $y).R
        $c2 = $bmp.GetPixel($x + 1, $y).R
        $diffSum += [math]::Abs($c1 - $c2)
        $count++
    }
}
$bmp.Dispose()
Write-Host "Nitidez resultante: $([math]::Round($diffSum / $count, 2))"
