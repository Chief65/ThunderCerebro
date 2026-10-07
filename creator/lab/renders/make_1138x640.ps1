param(
    [string]$InputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\menu_principal_taberna\menu_principal_taberna_9.jpg",
    [string]$OutputPath = "C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\menu_principal_taberna\menu_principal_taberna_1138x640.jpg"
)

Add-Type -AssemblyName System.Drawing

$srcImg = [System.Drawing.Image]::FromFile($InputPath)
$targetWidth = 1138
$targetHeight = 640

$destBmp = New-Object System.Drawing.Bitmap($targetWidth, $targetHeight)
$graphics = [System.Drawing.Graphics]::FromImage($destBmp)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

$srcRect = New-Object System.Drawing.Rectangle(0, 0, $srcImg.Width, $srcImg.Height)
$destRect = New-Object System.Drawing.Rectangle(0, 0, $targetWidth, $targetHeight)

$graphics.DrawImage($srcImg, $destRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)

$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
$encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
$encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]95)

$destBmp.Save($OutputPath, $codec, $encoderParams)

$graphics.Dispose()
$destBmp.Dispose()
$srcImg.Dispose()

Write-Host "Generado: $OutputPath"
Get-Item $OutputPath | Select-Object Name, Length
