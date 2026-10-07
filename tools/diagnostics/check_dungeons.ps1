echo "ls -1 Dungeons/region" | sftp -P 2022 -o BatchMode=yes ymykh9qy.575c7473@MIA-251006.bloom.host > "C:\Users\PC\Desktop\ThunderCerebro\dungeons_count.txt"
$count = (Get-Content "C:\Users\PC\Desktop\ThunderCerebro\dungeons_count.txt" | Measure-Object -Line).Lines
Write-Output "Dungeons region files: $count"
