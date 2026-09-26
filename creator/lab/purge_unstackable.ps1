$lines = Get-Content 'creator/lab/smartspawner_spawners_settings.yml'
$unstackable = @('BOW', 'CROSSBOW', 'GOLDEN_AXE', 'GOLDEN_SWORD', 'IRON_AXE', 'SADDLE', 'STONE_SWORD', 'TOTEM_OF_UNDYING', 'TRIDENT')

$newLines = @()
$skip = $false
$skipIndent = 0

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # Check if this line starts a loot item
    if ($line -match '^(\s{4})([A-Z_]+):') {
        $indent = $matches[1].Length
        $item = $matches[2]
        if ($unstackable -contains $item) {
            $skip = $true
            $skipIndent = $indent
            continue
        } else {
            $skip = $false
        }
    } elseif ($skip) {
        # Check if line is still indented inside the skipped block
        if ($line -match '^(\s+)') {
            $indent = $matches[1].Length
            if ($indent -gt $skipIndent) {
                continue # Skip child properties
            } else {
                $skip = $false
            }
        } else {
            $skip = $false
        }
    }
    
    $newLines += $line
}

[System.IO.File]::WriteAllLines('creator/lab/smartspawner_spawners_settings.yml', $newLines, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "Purge complete. Output lines: $($newLines.Count)"
