$dir = 'creator/lab'
for ($tier = 2; $tier -le 5; $tier++) {
    $path = Join-Path $dir "bolsadedinero_$tier.yml"
    $content = [System.IO.File]::ReadAllText($path)
    
    # Reemplazar colores en SEND_MESSAGE
    # Tier 2: &#0CCEE8 -> &#59E91F
    # Tier 3: &#BA0FFA -> &#59E91F
    # Tier 4: &#BC1013 -> &#59E91F
    # Tier 5: &#FAB60F -> &#59E91F
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, 'SEND_MESSAGE &#[A-Fa-f0-9]{6}&l\$', 'SEND_MESSAGE &#59E91F&l$')
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, 'SEND_MESSAGE &#[A-Fa-f0-9]{6}&l★', 'SEND_MESSAGE &#59E91F&l★')
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, 'conseguido &#[A-Fa-f0-9]{6}', 'conseguido &#59E91F')
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, 'maximo de &#[A-Fa-f0-9]{6}', 'maximo de &#59E91F')
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, 'supremo de &#[A-Fa-f0-9]{6}', 'supremo de &#59E91F')
    
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
    Write-Output "Actualizado chat de: bolsadedinero_$tier.yml"
}
