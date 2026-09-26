Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead('creator/lab/SCore.jar')
foreach ($entry in $zip.Entries) {
    if ($entry.FullName.EndsWith('.class')) {
        $stream = $entry.Open()
        $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::ASCII)
        $content = $reader.ReadToEnd()
        $reader.Close()
        $stream.Close()
        if ($content -match 'HIDE_ADDITIONAL_TOOLTIP' -or $content -match 'hideAdditionalTooltip') {
            Write-Output "Match: $($entry.FullName)"
        }
    }
}
$zip.Dispose()
