$dir = 'creator/lab'
for ($i = 1; $i -le 5; $i++) {
    $file = if ($i -eq 1) { 'vialdealmas.yml' } else { "vialdealmas_$i.yml" }
    $path = Join-Path $dir $file
    $content = [System.IO.File]::ReadAllText($path)
    
    $target = 'execute at %player% run playsound minecraft:entity.zombie.break_wooden_door master %player% ~ ~ ~ 0.9 1.1 +++ execute at %player% run playsound minecraft:block.amethyst_cluster.hit master %player% ~ ~ ~ 1.1 2.0'
    $replacement = $target + ' +++ execute at %player% run playsound minecraft:entity.vex.death master %player% ~ ~ ~ 0.85 1.25'
    
    if ($content.Contains($target)) {
        $content = $content.Replace($target, $replacement)
        [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
        Write-Output "Actualizado: $file"
    } else {
        Write-Output "No encontrado target en: $file"
    }
}
