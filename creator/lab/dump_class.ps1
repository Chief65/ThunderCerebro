$bytes = [System.IO.File]::ReadAllBytes('creator/lab/Hiders_full.class')
$text = [System.Text.Encoding]::ASCII.GetString($bytes)
$text -split "`0" | Where-Object { $_.Length -gt 3 } | Out-File -FilePath 'creator/lab/hiders_decomp.txt' -Encoding utf8
