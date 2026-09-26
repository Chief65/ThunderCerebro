$dir = 'creator/lab'
for ($tier = 1; $tier -le 5; $tier++) {
    $file = if ($tier -eq 1) { 'bolsadedinero.yml' } else { "bolsadedinero_$tier.yml" }
    $path = Join-Path $dir $file
    $content = [System.IO.File]::ReadAllText($path)
    
    # 1. Actualizar subtítulos durante la animación de apertura (blanco &f)
    $content = $content.Replace('subtitle "&2&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ..."', 'subtitle "&f&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ..."')
    $content = $content.Replace('subtitle "&a&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ..."', 'subtitle "&f&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ..."')
    $content = $content.Replace('subtitle "&a&o¡ᴅᴇꜱᴄɪꜰʀᴀᴅᴏ!"', 'subtitle "&f&o¡ᴅᴇꜱᴄɪꜰʀᴀᴅᴏ!"')
    
    # 2. Agregar sonido de saddle / bolsa de cuero al inicio de la animación
    # En la primera linea de sonido (amethyst hit 1.0)
    $oldSound1 = 'execute at %player% run playsound minecraft:block.amethyst_block.hit master %player% ~ ~ ~ 0.8 1.0'
    $newSound1 = "$oldSound1`n    - execute at %player% run playsound minecraft:entity.horse.saddle master %player% ~ ~ ~ 0.9 1.1"
    
    if ($content.Contains($oldSound1) -and -not $content.Contains('minecraft:entity.horse.saddle')) {
        $content = $content.Replace($oldSound1, $newSound1)
    }
    
    # 3. Actualizar subtítulos finales de recompensa a blanco &f
    $content = $content.Replace('subtitle "&a¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!"', 'subtitle "&f¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!"')
    $content = $content.Replace('subtitle "&a¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!"', 'subtitle "&f¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!"')
    $content = $content.Replace('subtitle "&a¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!"', 'subtitle "&f¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!"')
    
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
    Write-Output "Actualizado: $file"
}
