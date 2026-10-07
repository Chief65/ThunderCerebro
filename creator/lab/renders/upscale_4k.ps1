Add-Type -AssemblyName System.Drawing

function Optimize-And-Upscale-To-4K {
    param (
        [Parameter(Mandatory=$true)] [string]$InputPath,
        [Parameter(Mandatory=$true)] [string]$OutputPath,
        [int]$TargetWidth = 3840,
        [int]$TargetHeight = 2160
    )

    Write-Host "Cargando imagen: $InputPath"
    $src = [System.Drawing.Image]::FromFile($InputPath)
    
    # 1. Crear canvas 4K con máxima profundidad de color
    $destBmp = New-Object System.Drawing.Bitmap($TargetWidth, $TargetHeight, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $destBmp.SetResolution(300, 300)

    $g = [System.Drawing.Graphics]::FromImage($destBmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality

    $destRect = New-Object System.Drawing.Rectangle(0, 0, $TargetWidth, $TargetHeight)
    $g.DrawImage($src, $destRect)
    $g.Dispose()
    $src.Dispose()

    # 2. Guardar con calidad JPEG al 100% sin compresión visible
    $jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
    $encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
    $encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]100)

    $destBmp.Save($OutputPath, $jpegCodec, $encoderParams)
    $destBmp.Dispose()
    Write-Host "Activo 4K UHD guardado con éxito en: $OutputPath"
}
