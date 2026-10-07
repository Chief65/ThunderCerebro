$lines = Get-Content 'C:\Users\PC\Desktop\ThunderCerebro\plugins_scan_out.txt'
$currentDir = ""
$dirTotals = @{}

foreach ($l in $lines) {
    if ($l -match '^sftp>\s+ls\s+-lh\s+(.*)') {
        $currentDir = $matches[1].Trim()
        if (-not $dirTotals.ContainsKey($currentDir)) {
            $dirTotals[$currentDir] = [double]0
        }
        continue
    }
    
    if ($l -match '\s+([\d\.]+)([BKMGTbkmgt]?)\s+[A-Za-z]{3}\s+\d+\s+.*') {
        $val = [double]$matches[1]
        $unit = $matches[2].ToUpper()
        $multiplier = 1
        switch ($unit) {
            'K' { $multiplier = 1KB }
            'M' { $multiplier = 1MB }
            'G' { $multiplier = 1GB }
            'T' { $multiplier = 1TB }
            default { $multiplier = 1 }
        }
        if ($currentDir -ne "") {
            $dirTotals[$currentDir] += ($val * $multiplier)
        }
    }
}

$sorted = $dirTotals.GetEnumerator() | Sort-Object -Property Value -Descending
Write-Output "Top plugin directories by size:"
foreach ($item in $sorted | Select-Object -First 25) {
    $gb = [math]::Round($item.Value / 1GB, 3)
    $mb = [math]::Round($item.Value / 1MB, 2)
    Write-Output "$($item.Key) : $gb GB ($mb MB)"
}
