# Ejecutar en Windows PowerShell 5.1 o PowerShell 7 sobre Windows.
# Trabaja exclusivamente en una carpeta temporal y no inicia el servidor.
$ErrorActionPreference = 'Stop'
$source = Join-Path (Split-Path -Parent $PSScriptRoot) '_app\server.ps1'
$parseErrors = $null; $tokens = $null
$ast = [Management.Automation.Language.Parser]::ParseFile($source, [ref]$tokens, [ref]$parseErrors)
if ($parseErrors.Count) { throw ($parseErrors | Out-String) }
# Cargar las funciones del servidor real, sin ejecutar el listener.
foreach ($f in $ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] }, $false)) {
    . ([scriptblock]::Create($f.Extent.Text))
}
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$Root = Join-Path ([IO.Path]::GetTempPath()) ('noera-test-' + [Guid]::NewGuid().ToString('N'))
$AppDir = Join-Path $Root '_app'
$MetaFile = Join-Path $AppDir 'metadata.json'
$MaxExpandedZipBytes = 1MB
$MaxZipEntries = 20
$AllowedExt = @('.txt', '.md')
[void][IO.Directory]::CreateDirectory($AppDir)
function Assert($condition, [string]$message) { if (-not $condition) { throw "FAIL: $message" }; Write-Host "PASS: $message" }
function Reject([scriptblock]$action, [string]$message) {
    $failed = $false
    try { & $action } catch { $failed = $true }
    Assert $failed $message
}
function MakeZip([string]$path, [string[]]$names, [int]$size = 4) {
    $out = [IO.File]::Create($path)
    $zip = New-Object IO.Compression.ZipArchive($out, [IO.Compression.ZipArchiveMode]::Create, $true)
    try {
        foreach ($name in $names) {
            $entry = $zip.CreateEntry($name)
            $stream = $entry.Open()
            try { $b = New-Object byte[] $size; $stream.Write($b, 0, $b.Length) } finally { $stream.Dispose() }
        }
    } finally { $zip.Dispose(); $out.Dispose() }
}
try {
    $project = Join-Path $Root 'Proyecto'
    [void][IO.Directory]::CreateDirectory((Join-Path $project 'vacia'))
    [IO.File]::WriteAllText((Join-Path $project 'nota.txt'), 'original')
    [IO.File]::WriteAllBytes((Join-Path $project 'imagen.png'), [byte[]]@(0, 1, 2, 255))
    [IO.File]::WriteAllText((Join-Path $project '.config'), 'oculto')
    Assert ((Resolve-Rel 'Proyecto/nota.txt') -eq (Join-Path $project 'nota.txt')) 'Ruta normal'
    Reject { Resolve-Rel '../escape.txt' } 'Traversal rechazado'
    Reject { Resolve-Rel 'Proyecto./nota.txt' } 'Alias de Windows rechazado'
    Reject { Resolve-Rel 'Proyecto/CON.txt' } 'Dispositivo Windows rechazado'
    Reject { Resolve-Rel '_app/server.ps1' } 'Nucleo reservado'
    $backup = Join-Path $AppDir 'backup.zip'
    New-FolderZip $project $backup
    $zip = [IO.Compression.ZipFile]::OpenRead($backup)
    try {
        $names = @($zip.Entries | ForEach-Object { $_.FullName })
        Assert ($names -contains 'imagen.png') 'Backup conserva binarios'
        Assert ($names -contains '.config') 'Backup conserva archivos ocultos'
        Assert ($names -contains 'vacia/') 'Backup conserva carpetas vacias'
    } finally { $zip.Dispose() }
    $destination = Join-Path $AppDir 'dest'
    [void][IO.Directory]::CreateDirectory($destination)
    $bad = Join-Path $AppDir 'bad.zip'
    MakeZip $bad @('../escape.txt')
    Reject { Expand-ValidatedZip $bad $destination } 'ZIP traversal rechazado'
    [IO.File]::Delete($bad); MakeZip $bad @('A.txt', 'a.txt')
    Reject { Expand-ValidatedZip $bad $destination } 'ZIP con duplicados rechazado'
    [IO.File]::Delete($bad); MakeZip $bad @('CON.txt')
    Reject { Expand-ValidatedZip $bad $destination } 'ZIP con dispositivo rechazado'
    [IO.File]::Delete($bad); MakeZip $bad @('grande.txt') 1048577
    Reject { Expand-ValidatedZip $bad $destination } 'Limite de expansion ZIP'
    Assert ([IO.File]::ReadAllText((Join-Path $project 'nota.txt')) -eq 'original') 'Original intacto tras rechazos'
    $meta = [PSCustomObject]@{ taggedFolders = [PSCustomObject]@{ Proyecto = [PSCustomObject]@{ update = $true; history = @([PSCustomObject]@{ backupRel = '.history/Proyecto/old.zip' }) } } }
    Save-NoeraMeta $meta
    Move-FolderMeta 'Proyecto' 'Renombrado'
    $loaded = Get-NoeraMeta
    Assert ($loaded.taggedFolders.Renombrado.update) 'Etiqueta remapeada'
    Assert ($loaded.taggedFolders.Renombrado.history[0].backupRel -eq '.history/Proyecto/old.zip') 'Referencia historica preservada'
    Move-FolderMeta 'Renombrado' 'renombrado'
    Assert ((Get-NoeraMeta).taggedFolders.PSObject.Properties.Name -ccontains 'renombrado') 'Cambio de mayusculas en metadatos'
    $good = Join-Path $AppDir 'good.zip'; MakeZip $good @('nuevo.txt')
    Assert ((Expand-ValidatedZip $good $destination) -eq 1) 'ZIP valido extraido'
    Assert ([IO.File]::Exists((Join-Path $destination 'nuevo.txt'))) 'Contenido extraido'
    [IO.File]::WriteAllText($MetaFile, '{invalid')
    Reject { Get-NoeraMeta } 'JSON corrupto no se reemplaza por vacio'
    Write-Host 'Pruebas terminadas.' -ForegroundColor Green
} finally {
    if ([IO.Directory]::Exists($Root)) { Remove-Item -LiteralPath $Root -Recurse -Force }
}
