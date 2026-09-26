Add-Type -AssemblyName System.IO.Compression.FileSystem
$utf8 = New-Object System.Text.UTF8Encoding $false

# Leer el texto exacto de subtitulo de premio maximo y supremo de los viales
$vial1 = [System.IO.File]::ReadAllText('creator/lab/vialdealmas.yml', $utf8)
$vial5 = [System.IO.File]::ReadAllText('creator/lab/vialdealmas_5.yml', $utf8)

# Extraer el subtítulo blanco de premio maximo
$matchMax = [regex]::Match($vial1, 'subtitle "(&f¡[^"]+ᴍᴀxɪᴍᴏ!)"')
$whiteMax = $matchMax.Groups[1].Value

# Extraer el subtítulo blanco de premio supremo
$matchSup = [regex]::Match($vial5, 'subtitle "(&f¡[^"]+ꜱᴜᴘʀᴇᴍᴏ!)"')
$whiteSup = $matchSup.Groups[1].Value

Write-Output "White Max: $whiteMax"
Write-Output "White Sup: $whiteSup"

for ($tier = 1; $tier -le 5; $tier++) {
    $file = if ($tier -eq 1) { 'bolsadedinero.yml' } else { "bolsadedinero_$tier.yml" }
    $path = "creator/lab/$file"
    $content = [System.IO.File]::ReadAllText($path, $utf8)

    # Reemplazar cualquier variante de premio maximo con &a por el blanco
    $content = [regex]::Replace($content, 'subtitle "&a¡[^"]+ᴍᴀxɪᴍᴏ!"', "subtitle `"$whiteMax`"")
    $content = [regex]::Replace($content, 'subtitle "&a¡[^"]+ꜱᴜᴘʀᴇᴍᴏ!"', "subtitle `"$whiteSup`"")

    [System.IO.File]::WriteAllText($path, $content, $utf8)
    Write-Output "Actualizado max/sup en: $file"
}
