$utf8 = New-Object System.Text.UTF8Encoding $false
$saddle = 'execute at %player% run playsound minecraft:entity.horse.saddle master %player% ~ ~ ~ 0.9 1.1'

for ($tier = 1; $tier -le 5; $tier++) {
    $file = if ($tier -eq 1) { 'bolsadedinero.yml' } else { "bolsadedinero_$tier.yml" }
    $path = "creator/lab/$file"
    $content = [System.IO.File]::ReadAllText($path, $utf8)

    # 1. Quitar el sonido de saddle del inicio (tick 0)
    $content = $content.Replace("    - $saddle`n", '')
    $content = $content.Replace("    - $saddle`r`n", '')

    # 2. Agregar el sonido de saddle al final (en cada tirada de recompensa)
    # Patron comun en tiradas regulares: execute at %player% run playsound minecraft:entity.player.levelup master %player% ~ ~ ~ 1 1.5
    $target1 = 'execute at %player% run playsound minecraft:entity.player.levelup master %player% ~ ~ ~ 1 1.5'
    $replacement1 = "$target1 +++ $saddle"
    $content = $content.Replace($target1, $replacement1)

    # Patron en Premio Maximo / Supremo: execute at %player% run playsound minecraft:ui.toast.challenge_complete master %player% ~ ~ ~ 1 1.2
    $target2 = 'execute at %player% run playsound minecraft:ui.toast.challenge_complete master %player% ~ ~ ~ 1 1.2'
    $replacement2 = "$target2 +++ $saddle"
    $content = $content.Replace($target2, $replacement2)

    # Patron en Premio Supremo (Tier V pitch 1.0): execute at %player% run playsound minecraft:ui.toast.challenge_complete master %player% ~ ~ ~ 1 1.0
    $target3 = 'execute at %player% run playsound minecraft:ui.toast.challenge_complete master %player% ~ ~ ~ 1 1.0'
    $replacement3 = "$target3 +++ $saddle"
    $content = $content.Replace($target3, $replacement3)

    [System.IO.File]::WriteAllText($path, $content, $utf8)
    Write-Output "Movido saddle al final en: $file"
}
