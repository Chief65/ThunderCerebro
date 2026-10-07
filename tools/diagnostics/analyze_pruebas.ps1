$lines = Get-Content 'C:\Users\PC\Desktop\ThunderCerebro\pruebas_scan_out.txt'
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

foreach ($k in $dirTotals.Keys) {
    $gb = [math]::Round($dirTotals[$k] / 1GB, 3)
    $mb = [math]::Round($dirTotals[$k] / 1MB, 2)
    Write-Output "$k : $gb GB ($mb MB)"
}
