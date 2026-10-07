# Read first 100 lines from end_files_names.txt
$files = Get-Content "C:\Users\PC\Desktop\ThunderCerebro\end_files_names.txt" | Select-Object -First 50
$sb = [System.Text.StringBuilder]::new()
foreach ($f in $files) {
    $clean = $f.Trim()
    if ($clean -like '*.mca') {
        [void]$sb.AppendLine("ls -lh $clean")
    }
}
[void]$sb.AppendLine("bye")
[System.IO.File]::WriteAllText("C:\Users\PC\Desktop\ThunderCerebro\sftp_sample_end.txt", $sb.ToString())
Write-Output "Prepared sample for $($files.Count) End region files"
