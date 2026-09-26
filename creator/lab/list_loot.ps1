$lines = Get-Content 'creator/lab/smartspawner_spawners_settings.yml'
$lootItems = @()
$currentMob = ''
$inLoot = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '^([A-Z_]+):') {
        $currentMob = $matches[1]
        $inLoot = $false
    }
    if ($line -match '^\s{2}loot:') {
        $inLoot = $true
        continue
    }
    if ($line -match '^\s{2}[a-z_]+:') {
        $inLoot = $false
    }
    if ($inLoot -and ($line -match '^\s{4}([A-Z_]+):')) {
        $lootItems += [PSCustomObject]@{ Mob = $currentMob; Item = $matches[1]; Line = ($i+1) }
    }
}
$lootItems | Group-Object Item | ForEach-Object {
    [PSCustomObject]@{
        Item = $_.Name
        Count = $_.Count
        Mobs = ($_.Group.Mob -join ', ')
    }
} | Sort-Object Item | Format-Table -AutoSize
