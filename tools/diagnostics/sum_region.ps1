$lines = Get-Content 'C:\Users\PC\Desktop\ThunderCerebro\region_list.txt'
$totalBytes = [double]0
$count = 0

foreach ($l in $lines) {
    if ($l -match '\s+([\d\.]+)([BKMGTbkmgt]?)\s+[A-Za-z]{3}\s+\d+\s+.*\.mca') {
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
        $totalBytes += ($val * $multiplier)
        $count++
    }
}
Write-Output "MCA files count: $count"
Write-Output "Total world/region size: $([math]::Round($totalBytes / 1GB, 2)) GB ($([math]::Round($totalBytes / 1MB, 2)) MB)"
