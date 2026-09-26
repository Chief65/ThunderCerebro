$utf8 = New-Object System.Text.UTF8Encoding $false
for ($tier = 1; $tier -le 5; $tier++) {
    $file = if ($tier -eq 1) { 'bolsadedinero.yml' } else { "bolsadedinero_$tier.yml" }
    $path = "creator/lab/$file"
    $content = [System.IO.File]::ReadAllText($path, $utf8)

    # Reemplazo de subtítulos de animación a &f
    $content = $content.Replace('&2&o' + [char]0x1D05 + [char]0x1D07 + [char]0xA731 + [char]0x1D04 + [char]0x026A + [char]0xA730 + [char]0x0280 + [char]0x1D00 + [char]0x0274 + [char]0x1D05 + '...', '&f&o' + [char]0x1D05 + [char]0x1D07 + [char]0xA731 + [char]0x1D04 + [char]0x026A + [char]0xA730 + [char]0x0280 + [char]0x1D00 + [char]0x0274 + [char]0x1D05 + '...')
    $content = $content.Replace('&a&o' + [char]0x1D05 + [char]0x1D07 + [char]0xA731 + [char]0x1D04 + [char]0x026A + [char]0xA730 + [char]0x0280 + [char]0x1D00 + [char]0x0274 + [char]0x1D05 + '...', '&f&o' + [char]0x1D05 + [char]0x1D07 + [char]0xA731 + [char]0x1D04 + [char]0x026A + [char]0xA730 + [char]0x0280 + [char]0x1D00 + [char]0x0274 + [char]0x1D05 + '...')
    $content = $content.Replace('&a&o' + [char]0x00A1 + [char]0x1D05 + [char]0x1D07 + [char]0xA731 + [char]0x1D04 + [char]0x026A + [char]0xA730 + [char]0x0280 + [char]0x1D00 + [char]0x1D05 + [char]0x1D0F + '!', '&f&o' + [char]0x00A1 + [char]0x1D05 + [char]0x1D07 + [char]0xA731 + [char]0x1D04 + [char]0x026A + [char]0xA730 + [char]0x0280 + [char]0x1D00 + [char]0x1D05 + [char]0x1D0F + '!')

    # Reemplazo de subtítulos de recompensa a &f
    $content = $content.Replace('subtitle "&a' + [char]0x00A1 + [char]0x0280 + [char]0x1D07 + [char]0x1D04 + [char]0x1D0F + [char]0x1D0D + [char]0x1D18 + [char]0x1D07 + [char]0x0274 + [char]0xA731 + [char]0x1D00 + ' ' + [char]0x1D0F + [char]0x0299 + [char]0x1D1B + [char]0x1D07 + [char]0x0274 + [char]0x026A + [char]0x1D05 + [char]0x1D00 + '!"', 'subtitle "&f' + [char]0x00A1 + [char]0x0280 + [char]0x1D07 + [char]0x1D04 + [char]0x1D0F + [char]0x1D0D + [char]0x1D18 + [char]0x1D07 + [char]0x0274 + [char]0xA731 + [char]0x1D00 + ' ' + [char]0x1D0F + [char]0x0299 + [char]0x1D1B + [char]0x1D07 + [char]0x0274 + [char]0x026A + [char]0x1D05 + [char]0x1D00 + '!"')
    $content = $content.Replace('subtitle "&a' + [char]0x00A1 + [char]0x1D18 + [char]0x0280 + [char]0x1D07 + [char]0x1D0D + [char]0x026A + [char]0x1D0F + ' ' + [char]0x1D0D + [char]0x1D00 + [char]0x0278 + [char]0x026A + [char]0x1D0D + [char]0x1D0F + '!"', 'subtitle "&f' + [char]0x00A1 + [char]0x1D18 + [char]0x0280 + [char]0x1D07 + [char]0x1D0D + [char]0x026A + [char]0x1D0F + ' ' + [char]0x1D0D + [char]0x1D00 + [char]0x0278 + [char]0x026A + [char]0x1D0D + [char]0x1D0F + '!"')
    $content = $content.Replace('subtitle "&a' + [char]0x00A1 + [char]0x1D18 + [char]0x0280 + [char]0x1D07 + [char]0x1D0D + [char]0x026A + [char]0x1D0F + ' ' + [char]0xA731 + [char]0x1D18 + [char]0x0280 + [char]0x1D07 + [char]0x1D0D + [char]0x1D0F + '!"', 'subtitle "&f' + [char]0x00A1 + [char]0x1D18 + [char]0x0280 + [char]0x1D07 + [char]0x1D0D + [char]0x026A + [char]0x1D0F + ' ' + [char]0xA731 + [char]0x1D18 + [char]0x0280 + [char]0x1D07 + [char]0x1D0D + [char]0x1D0F + '!')

    # Insertar sonido saddle si no existe
    $saddle = 'execute at %player% run playsound minecraft:entity.horse.saddle master %player% ~ ~ ~ 0.9 1.1'
    if (-not $content.Contains($saddle)) {
        $target = 'execute at %player% run playsound minecraft:block.amethyst_block.hit master %player% ~ ~ ~ 0.8 1.0'
        $replacement = "$target`n    - $saddle"
        $content = $content.Replace($target, $replacement)
    }

    [System.IO.File]::WriteAllText($path, $content, $utf8)
    Write-Output "Actualizado: $file"
}
