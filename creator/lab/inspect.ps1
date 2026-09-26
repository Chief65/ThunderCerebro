$bytes = [System.IO.File]::ReadAllBytes('creator/lab/Hiders.class')
$text = [System.Text.Encoding]::ASCII.GetString($bytes)
$matches = [regex]::Matches($text, '[A-Za-z0-9_]{3,}')
$filtered = @()
foreach ($m in $matches) {
    if ($m.Value -match '(?i)hide|potion|tooltip|ominous') {
        $filtered += $m.Value
    }
}
$filtered | Select-Object -Unique | Out-File -FilePath 'creator/lab/hiders_strings.txt' -Encoding utf8
