$bytesIn = [System.IO.File]::ReadAllBytes('creator/lab/level.dat')
$msIn = New-Object System.IO.MemoryStream(,$bytesIn)
$gzip = New-Object System.IO.Compression.GZipStream($msIn, [System.IO.Compression.CompressionMode]::Decompress)
$msOut = New-Object System.IO.MemoryStream
$buffer = New-Object byte[] 4096
while (($count = $gzip.Read($buffer, 0, $buffer.Length)) -gt 0) {
    $msOut.Write($buffer, 0, $count)
}
$decompressed = $msOut.ToArray()
$str = [System.Text.Encoding]::ASCII.GetString($decompressed)
[regex]::Matches($str, '[a-zA-Z0-9_]{3,}') | ForEach-Object { $_.Value } | Select-Object -Unique
