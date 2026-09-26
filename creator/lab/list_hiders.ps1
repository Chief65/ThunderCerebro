Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead('creator/lab/SCore.jar')
foreach ($entry in $zip.Entries) {
    if ($entry.FullName -like '*hiders*') {
        Write-Output $entry.FullName
    }
}
$zip.Dispose()
