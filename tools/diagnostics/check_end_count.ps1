echo "ls -1 world_the_end/DIM1/region" | sftp -P 2022 -o BatchMode=yes ymykh9qy.575c7473@MIA-251006.bloom.host > "C:\Users\PC\Desktop\ThunderCerebro\end_files_names.txt"
$count = (Get-Content "C:\Users\PC\Desktop\ThunderCerebro\end_files_names.txt" | Measure-Object -Line).Lines
Write-Output "Lines returned: $count"
