<#
  Noera - servidor local del explorador de archivos.
  - Escucha SOLO en 127.0.0.1 (no accesible desde la red).
  - Opera SOLO dentro de la carpeta Noera (padre de _app). Cualquier ruta fuera se rechaza.
  - Solo gestiona extensiones de la lista $AllowedExt.
  - "Eliminar" mueve a Noera\.papelera (nunca borra de forma definitiva).
  Uso: iniciar-noera.bat   (o: powershell -ExecutionPolicy Bypass -File server.ps1)
#>
param([ValidateRange(1024, 65526)][int]$Port = 7710, [switch]$NoBrowser)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Web
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$AppDir = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $AppDir '..')).Path.TrimEnd('\')
$AllowedExt = @('.md', '.txt', '.json', '.yml', '.yaml', '.xml', '.csv', '.toml', '.ini', '.cfg', '.properties', '.html', '.css', '.js')
$MaxEditBytes = 2MB
$MaxUploadBytes = 150MB
$MaxFileUploadBytes = 25MB
$MaxExpandedZipBytes = 1GB
$MaxZipEntries = 20000
$Token = [Guid]::NewGuid().ToString('N')
$Utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)
$MetaFile = Join-Path $AppDir 'metadata.json'

# Escritura con reemplazo: el JSON anterior sigue íntegro si falla la escritura.
function Write-AtomicText([string]$path, [string]$text) {
    $tmp = "$path.$([Guid]::NewGuid().ToString('N')).tmp"
    try {
        [IO.File]::WriteAllText($tmp, $text, (New-Object Text.UTF8Encoding($false)))
        if ([IO.File]::Exists($path)) { [IO.File]::Replace($tmp, $path, [NullString]::Value) }
        else { [IO.File]::Move($tmp, $path) }
    } finally { if ([IO.File]::Exists($tmp)) { [IO.File]::Delete($tmp) } }
}

function Assert-NoReparse([string]$full) {
    $cursor = $full
    while ($cursor -and $cursor.Length -ge $Root.Length) {
        if ([IO.File]::Exists($cursor) -or [IO.Directory]::Exists($cursor)) {
            if (([IO.File]::GetAttributes($cursor) -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                Fail 403 'No se permite atravesar enlaces simbólicos ni uniones de carpetas.'
            }
        }
        if ($cursor -ieq $Root) { break }
        $cursor = [IO.Path]::GetDirectoryName($cursor)
    }
}

function Move-FolderMeta([string]$oldPath, [string]$newPath) {
    $meta = Get-NoeraMeta
    $keys = @($meta.taggedFolders.PSObject.Properties | ForEach-Object { $_.Name })
    foreach ($key in $keys) {
        if ($key -ieq $oldPath -or $key.StartsWith($oldPath + '/', [StringComparison]::OrdinalIgnoreCase)) {
            $value = $meta.taggedFolders.PSObject.Properties[$key].Value
            $meta.taggedFolders.PSObject.Properties.Remove($key)
            if ($newPath) {
                $newKey = $newPath + $key.Substring($oldPath.Length)
                # backupRel apunta al respaldo original: no se reescribe.
                $meta.taggedFolders | Add-Member -MemberType NoteProperty -Name $newKey -Value $value -Force
            }
        }
    }
    Save-NoeraMeta $meta
}

function Attachment-Headers([string]$name) {
    return @{ 'Content-Disposition' = "attachment; filename=download; filename*=UTF-8''$([Uri]::EscapeDataString($name))" }
}

function Send-File($ctx, [string]$full, [string]$ctype, [string]$name) {
    $inputFile = [IO.File]::OpenRead($full)
    try {
        $r = $ctx.Response
        $r.StatusCode = 200; $r.ContentType = $ctype
        $r.Headers['Cache-Control'] = 'no-store'
        $r.Headers['X-Content-Type-Options'] = 'nosniff'
        $r.Headers['Referrer-Policy'] = 'no-referrer'
        $r.Headers['Content-Security-Policy'] = "default-src 'none'; sandbox"
        $headers = Attachment-Headers $name
        $r.Headers['Content-Disposition'] = $headers['Content-Disposition']
        $r.ContentLength64 = $inputFile.Length
        $inputFile.CopyTo($r.OutputStream)
    } finally { $inputFile.Dispose(); $ctx.Response.OutputStream.Close() }
}

function Get-NoeraMeta() {
    if (Test-Path -LiteralPath $MetaFile) {
        try {
            $raw = [IO.File]::ReadAllText($MetaFile, [Text.Encoding]::UTF8)
            $m = ($raw | ConvertFrom-Json)
            if ($m -and $m.taggedFolders -is [PSCustomObject]) { return $m }
            Fail 500 'metadata.json no tiene un formato válido. Conserva el archivo y revisa su contenido.'
        } catch { Fail 500 'No se pueden leer los metadatos; se conservan para evitar pérdida de historial.' }
    }
    return [PSCustomObject]@{ taggedFolders = [PSCustomObject]@{} }
}

function Save-NoeraMeta($meta) {
    $raw = ConvertTo-Json -InputObject $meta -Depth 10
    Write-AtomicText $MetaFile $raw
}

$Static = @{
    '/'           = @('index.html', 'text/html; charset=utf-8')
    '/index.html' = @('index.html', 'text/html; charset=utf-8')
    '/app.css'    = @('app.css', 'text/css; charset=utf-8')
    '/app.js'     = @('app.js', 'application/javascript; charset=utf-8')
}

# ---------- utilidades ----------
function Fail([int]$code, [string]$msg) { throw "API|$code|$msg" }

function Send-Bytes($ctx, [int]$status, [string]$ctype, [byte[]]$bytes, [hashtable]$headers = $null) {
    $r = $ctx.Response
    try {
        $r.StatusCode = $status
        $r.ContentType = $ctype
        $r.Headers['Cache-Control'] = 'no-store'
        $r.Headers['X-Content-Type-Options'] = 'nosniff'
        $r.Headers['Referrer-Policy'] = 'no-referrer'
        $r.Headers['Content-Security-Policy'] = "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
        if ($headers) {
            foreach ($k in $headers.Keys) { $r.Headers[$k] = [string]$headers[$k] }
        }
        $r.ContentLength64 = $bytes.Length
        $r.OutputStream.Write($bytes, 0, $bytes.Length)
    }
    finally { $r.OutputStream.Close() }
}

function Send-Json($ctx, [int]$status, $obj) {
    $json = ConvertTo-Json -InputObject $obj -Depth 100 -Compress
    Send-Bytes $ctx $status 'application/json; charset=utf-8' ([Text.Encoding]::UTF8.GetBytes($json))
}

function Read-Body($req, [long]$max) {
    if ($req.ContentLength64 -gt $max) { Fail 413 'Contenido demasiado grande.' }
    $ms = New-Object IO.MemoryStream
    $buf = New-Object byte[] 81920
    try {
        while (($n = $req.InputStream.Read($buf, 0, $buf.Length)) -gt 0) {
            if ($ms.Length + $n -gt $max) { Fail 413 'Contenido demasiado grande.' }
            $ms.Write($buf, 0, $n)
        }
        return , $ms.ToArray()
    } finally { $ms.Dispose() }
}

function Read-JsonBody($req) {
    $bytes = Read-Body $req 1MB
    try {
        $obj = $Utf8Strict.GetString($bytes) | ConvertFrom-Json
        if ($null -eq $obj -or $obj -isnot [PSCustomObject]) { Fail 400 'Se requiere un objeto JSON.' }
        return $obj
    }
    catch { Fail 400 'JSON inválido.' }
}

function Test-Name([string]$name, [bool]$isFile) {
    if ([string]::IsNullOrWhiteSpace($name)) { return 'El nombre está vacío.' }
    if ($name.Length -gt 120) { return 'El nombre es demasiado largo (máx. 120).' }
    if ($name -match '[\\/:*?"<>|\x00-\x1f]') { return 'Caracteres no permitidos: \ / : * ? " < > |' }
    if ($name -ne $name.Trim() -or $name.EndsWith('.')) { return 'No puede empezar/terminar con espacios ni terminar en punto.' }
    if ($name.StartsWith('.') -or $name.StartsWith('_')) { return 'No puede empezar con "." ni "_" (reservado).' }
    if ($name -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$') { return 'Nombre reservado de Windows.' }
    if ($isFile) {
        $ext = [IO.Path]::GetExtension($name).ToLowerInvariant()
        if ($AllowedExt -notcontains $ext) { return "Extensión no permitida ($ext). Permitidas: $($AllowedExt -join ' ')" }
    }
    return $null
}

function Assert-Name([string]$name, [bool]$isFile) {
    $e = Test-Name $name $isFile
    if ($e) { Fail 400 $e }
}

function Resolve-Rel([string]$rel, [bool]$allowRoot = $false) {
    if ($null -eq $rel) { $rel = '' }
    $rel = $rel.Replace('/', '\').Trim('\')
    if ($rel -eq '') {
        if ($allowRoot) { Assert-NoReparse $Root; return $Root }
        Fail 400 'Ruta vacía.'
    }
    foreach ($seg in $rel.Split('\')) {
        if ($seg -ne $seg.Trim() -or $seg.EndsWith('.') -or $seg -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$') { Fail 400 'Ruta ambigua o reservada en Windows.' }
        if ($seg -eq '' -or $seg.StartsWith('.') -or $seg.StartsWith('_') -or $seg -match '[:*?"<>|\x00-\x1f]') { Fail 400 'Ruta inválida.' }
    }
    $full = [IO.Path]::GetFullPath((Join-Path $Root $rel))
    if (-not $full.StartsWith($Root + '\', [StringComparison]::OrdinalIgnoreCase)) { Fail 400 'Ruta fuera de Noera.' }
    Assert-NoReparse $full
    return $full
}

function To-Rel([string]$full) { return $full.Substring($Root.Length + 1).Replace('\', '/') }

function Assert-Managed([string]$full) {
    if (Test-Path -LiteralPath $full -PathType Leaf) {
        $ext = [IO.Path]::GetExtension($full).ToLowerInvariant()
        if ($AllowedExt -notcontains $ext) { Fail 403 'Tipo de archivo no gestionado por Noera.' }
    }
    elseif (-not (Test-Path -LiteralPath $full -PathType Container)) { Fail 404 'No existe.' }
}

function Get-UniqueName([string]$dir, [string]$name) {
    $base = [IO.Path]::GetFileNameWithoutExtension($name)
    $ext = [IO.Path]::GetExtension($name)
    $n = $name; $i = 1
    while (Test-Path -LiteralPath (Join-Path $dir $n)) { $n = "$base ($i)$ext"; $i++ }
    return $n
}

function Test-Hidden($item) {
    return ($item.Name.StartsWith('.') -or $item.Name.StartsWith('_') -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint))
}

function Get-Children([string]$dir) {
    $dirs = Get-ChildItem -LiteralPath $dir -Directory -Force -ErrorAction SilentlyContinue | Where-Object { -not (Test-Hidden $_) } | Sort-Object Name
    foreach ($d in $dirs) {
        @{ type = 'dir'; name = $d.Name; path = (To-Rel $d.FullName); mtime = $d.LastWriteTimeUtc.Ticks.ToString(); children = @(Get-Children $d.FullName) }
    }
    $files = Get-ChildItem -LiteralPath $dir -File -Force -ErrorAction SilentlyContinue |
        Where-Object { -not (Test-Hidden $_) -and ($AllowedExt -contains $_.Extension.ToLowerInvariant()) } | Sort-Object Name
    foreach ($f in $files) {
        @{ type = 'file'; name = $f.Name; path = (To-Rel $f.FullName); ext = $f.Extension.ToLowerInvariant(); size = $f.Length; mtime = $f.LastWriteTimeUtc.Ticks.ToString() }
    }
}

function Write-FolderToZip($zip, [string]$dirPath, [string]$prefix) {
    Assert-NoReparse $dirPath
    if ($prefix) { [void]$zip.CreateEntry("$prefix/") }
    $items = @(Get-ChildItem -LiteralPath $dirPath -Force -ErrorAction Stop | Sort-Object Name)
    foreach ($item in $items) {
        # En la raíz no se exportan el núcleo, la papelera ni el historial.
        if ($dirPath -ieq $Root -and (Test-Hidden $item)) { continue }
        Assert-NoReparse $item.FullName
        $entryName = if ($prefix) { "$prefix/$($item.Name)" } else { $item.Name }
        if ($item.PSIsContainer) { Write-FolderToZip $zip $item.FullName $entryName }
        else {
            $entry = $zip.CreateEntry($entryName, [IO.Compression.CompressionLevel]::Optimal)
            $output = $entry.Open()
            $inputFile = $null
            try { $inputFile = [IO.File]::OpenRead($item.FullName); $inputFile.CopyTo($output) }
            finally { if ($inputFile) { $inputFile.Dispose() }; $output.Dispose() }
        }
    }
}

function New-FolderZip([string]$dir, [string]$destination) {
    $output = [IO.File]::Open($destination, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    $zip = $null
    try {
        $zip = New-Object IO.Compression.ZipArchive($output, [IO.Compression.ZipArchiveMode]::Create, $true)
        Write-FolderToZip $zip $dir ''
    } finally { if ($zip) { $zip.Dispose() }; $output.Dispose() }
}

function Expand-ValidatedZip([string]$zipFile, [string]$destination) {
    $zip = $null
    try {
        try { $zip = [IO.Compression.ZipFile]::OpenRead($zipFile) }
        catch { Fail 400 'El ZIP está dañado o no es válido.' }
        if ($zip.Entries.Count -eq 0) { Fail 400 'El ZIP está vacío; no se sustituye la carpeta.' }
        if ($zip.Entries.Count -gt $MaxZipEntries) { Fail 413 'El ZIP supera las 20000 entradas.' }
        $seen = @{}; $plan = @(); [long]$total = 0
        foreach ($entry in $zip.Entries) {
            $name = $entry.FullName.Replace('\', '/')
            if ($name.StartsWith('/') -or $name -match '[\x00-\x1f:*?"<>|]') { Fail 400 'El ZIP contiene una ruta no permitida.' }
            $isDir = $name.EndsWith('/')
            $clean = $name.TrimEnd('/')
            if (-not $clean) { Fail 400 'El ZIP contiene una ruta vacía.' }
            foreach ($part in $clean.Split('/')) {
                if (-not $part -or $part -eq '.' -or $part -eq '..' -or $part -ne $part.Trim() -or $part.EndsWith('.') -or $part -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$') {
                    Fail 400 'El ZIP contiene rutas ambiguas o reservadas.'
                }
            }
            # Atributos POSIX: se rechazan enlaces simbólicos (0120000).
            if ((($entry.ExternalAttributes -shr 16) -band 0xF000) -eq 0xA000) { Fail 400 'El ZIP contiene enlaces simbólicos.' }
            if ($seen.ContainsKey($clean)) { Fail 400 'El ZIP contiene nombres duplicados (sin distinguir mayúsculas).' }
            $seen[$clean] = $isDir
            $target = [IO.Path]::GetFullPath((Join-Path $destination ($clean.Replace('/', '\'))))
            if (-not $target.StartsWith($destination + '\', [StringComparison]::OrdinalIgnoreCase)) { Fail 400 'El ZIP intenta salir de la carpeta destino.' }
            $total += $entry.Length
            if ($total -gt $MaxExpandedZipBytes) { Fail 413 'El ZIP supera 1 GB descomprimido.' }
            $plan += @{ entry = $entry; path = $target; dir = $isDir }
        }
        # Validar todo antes de escribir; FileMode.CreateNew evita sobrescrituras.
        [long]$written = 0
        $buffer = New-Object byte[] 81920
        foreach ($item in $plan) {
            if ($item.dir) { [void][IO.Directory]::CreateDirectory($item.path); continue }
            [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($item.path))
            $inputFile = $item.entry.Open(); $output = $null
            try {
                $output = [IO.File]::Open($item.path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
                [long]$entryWritten = 0
                while (($n = $inputFile.Read($buffer, 0, $buffer.Length)) -gt 0) {
                    $written += $n; $entryWritten += $n
                    if ($written -gt $MaxExpandedZipBytes -or $entryWritten -gt $item.entry.Length) { Fail 413 'Contenido expandido excesivo.' }
                    $output.Write($buffer, 0, $n)
                }
                if ($entryWritten -ne $item.entry.Length) { Fail 400 'Entrada ZIP incompleta.' }
            } finally { $inputFile.Dispose(); if ($output) { $output.Dispose() } }
        }
        return $zip.Entries.Count
    } finally { if ($zip) { $zip.Dispose() } }
}

# ---------- manejo de peticiones ----------
function Handle($ctx) {
    $req = $ctx.Request
    $method = $req.HttpMethod
    $path = $req.Url.AbsolutePath

    if ($req.Headers['Host'] -ne "127.0.0.1:$Port") { Fail 403 'Host no permitido.' }

    if ($method -eq 'GET' -and $Static.ContainsKey($path)) {
        $file = Join-Path $AppDir $Static[$path][0]
        if (-not (Test-Path -LiteralPath $file)) { Fail 404 'Recurso de la aplicación no encontrado.' }
        $text = [IO.File]::ReadAllText($file, [Text.Encoding]::UTF8).Replace('{{TOKEN}}', $Token)
        Send-Bytes $ctx 200 $Static[$path][1] ([Text.Encoding]::UTF8.GetBytes($text))
        return
    }

    if ($req.Headers['Origin'] -and $req.Headers['Origin'] -cne "http://127.0.0.1:$Port") { Fail 403 'Origen no permitido.' }
    if (-not $path.StartsWith('/api/')) { Fail 404 'No encontrado.' }
    $q = [Web.HttpUtility]::ParseQueryString($req.Url.Query)
    $tokenHeader = $req.Headers['X-Noera-Token']
    if ($tokenHeader -cne $Token) { Fail 403 'Token inválido. Recarga la página.' }

    switch ("$method $path") {

        'GET /api/tree' {
            Send-Json $ctx 200 @{ root = 'Noera'; allowedExt = $AllowedExt; tree = @(Get-Children $Root) }
            return
        }

        'GET /api/download' {
            $full = Resolve-Rel $q['path']
            if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { Fail 404 'El archivo no existe.' }
            Assert-Managed $full
            Send-File $ctx $full 'application/octet-stream' (Split-Path -Leaf $full)
            return
        }

        'GET /api/file' {
            $full = Resolve-Rel $q['path']
            if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { Fail 404 'El archivo no existe.' }
            Assert-Managed $full
            $fi = Get-Item -LiteralPath $full
            if ($fi.Length -gt $MaxEditBytes) { Fail 413 'Archivo demasiado grande para abrirlo (máx. 2 MB).' }
            $bytes = [IO.File]::ReadAllBytes($full)
            if ($bytes -contains 0) { Fail 415 'El archivo no es texto.' }
            try { $text = $Utf8Strict.GetString($bytes) }
            catch { Fail 415 'El archivo no es UTF-8 válido; no se abre para evitar corromperlo.' }
            if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { $text = $text.Substring(1) }
            Send-Json $ctx 200 @{ path = (To-Rel $full); name = $fi.Name; content = $text; size = $fi.Length; mtime = $fi.LastWriteTimeUtc.Ticks.ToString() }
            return
        }

        'PUT /api/file' {
            $full = Resolve-Rel $q['path']
            if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { Fail 404 'El archivo no existe.' }
            Assert-Managed $full
            $expected = $q['mtime']
            if ($expected -and ((Get-Item -LiteralPath $full).LastWriteTimeUtc.Ticks.ToString() -ne $expected)) {
                Fail 409 'El archivo cambió en disco desde que lo abriste.'
            }
            $bytes = Read-Body $req $MaxEditBytes
            try { [void]$Utf8Strict.GetString($bytes) } catch { Fail 400 'El contenido no es UTF-8 válido.' }
            if ($bytes -contains 0) { Fail 400 'El contenido contiene bytes nulos.' }
            if ($expected -and ((Get-Item -LiteralPath $full).LastWriteTimeUtc.Ticks.ToString() -ne $expected)) { Fail 409 'El archivo cambió durante el guardado.' }
            $original = New-Object byte[] 3
            $originalStream = [IO.File]::OpenRead($full)
            try { $prefixLength = $originalStream.Read($original, 0, 3) } finally { $originalStream.Dispose() }
            if ($prefixLength -eq 3 -and $original[0] -eq 239 -and $original[1] -eq 187 -and $original[2] -eq 191) {
                $bytes = [byte[]](@(239, 187, 191) + $bytes)
            }
            $tmp = "$full.$([Guid]::NewGuid().ToString('N')).noera-tmp"
            try {
                [IO.File]::WriteAllBytes($tmp, $bytes)
                [IO.File]::Replace($tmp, $full, [NullString]::Value)
            }
            finally { if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue } }
            $fi = Get-Item -LiteralPath $full
            Send-Json $ctx 200 @{ mtime = $fi.LastWriteTimeUtc.Ticks.ToString(); size = $fi.Length }
            return
        }

        'POST /api/mkdir' {
            $b = Read-JsonBody $req
            $full = Resolve-Rel $b.path
            Assert-Name (Split-Path -Leaf $full) $false
            if (-not (Test-Path -LiteralPath (Split-Path -Parent $full) -PathType Container)) { Fail 404 'La carpeta padre no existe.' }
            if (Test-Path -LiteralPath $full) { Fail 409 'Ya existe un elemento con ese nombre.' }
            [void][IO.Directory]::CreateDirectory($full)
            Send-Json $ctx 200 @{ path = (To-Rel $full) }
            return
        }

        'POST /api/newfile' {
            $b = Read-JsonBody $req
            $full = Resolve-Rel $b.path
            Assert-Name (Split-Path -Leaf $full) $true
            if (-not (Test-Path -LiteralPath (Split-Path -Parent $full) -PathType Container)) { Fail 404 'La carpeta padre no existe.' }
            if (Test-Path -LiteralPath $full) { Fail 409 'Ya existe un elemento con ese nombre.' }
            [IO.File]::WriteAllBytes($full, [byte[]]@())
            Send-Json $ctx 200 @{ path = (To-Rel $full) }
            return
        }

        'POST /api/rename' {
            $b = Read-JsonBody $req
            $full = Resolve-Rel $b.path
            Assert-Managed $full
            $isFile = Test-Path -LiteralPath $full -PathType Leaf
            $newName = [string]$b.newName
            Assert-Name $newName $isFile
            $target = Join-Path (Split-Path -Parent $full) $newName
            if ($target -ceq $full) { Send-Json $ctx 200 @{ path = (To-Rel $full) }; return }
            $sameItem = ($target -ieq $full)
            if ((Test-Path -LiteralPath $target) -and -not $sameItem) { Fail 409 'Ya existe un elemento con ese nombre.' }
            if ($sameItem) {
                $tmp = Join-Path (Split-Path -Parent $full) ("noera-rename-" + [Guid]::NewGuid().ToString('N'))
                if ($isFile) {
                    [IO.File]::Move($full, $tmp)
                    try { [IO.File]::Move($tmp, $target) } catch { [IO.File]::Move($tmp, $full); throw }
                } else {
                    [IO.Directory]::Move($full, $tmp)
                    try { [IO.Directory]::Move($tmp, $target) } catch { [IO.Directory]::Move($tmp, $full); throw }
                }
            }
            elseif ($isFile) { [IO.File]::Move($full, $target) }
            else { [IO.Directory]::Move($full, $target) }
            try { if (-not $isFile) { Move-FolderMeta (To-Rel $full) (To-Rel $target) } }
            catch { if (-not $isFile) { [IO.Directory]::Move($target, $full) }; throw }
            Send-Json $ctx 200 @{ path = (To-Rel $target) }
            return
        }

        'POST /api/move' {
            $b = Read-JsonBody $req
            $src = Resolve-Rel $b.from
            $dest = Resolve-Rel $b.toDir $true
            Assert-Managed $src
            if (-not (Test-Path -LiteralPath $dest -PathType Container)) { Fail 404 'La carpeta destino no existe.' }
            $isFile = Test-Path -LiteralPath $src -PathType Leaf
            if (-not $isFile -and (($dest + '\').StartsWith($src + '\', [StringComparison]::OrdinalIgnoreCase))) { Fail 400 'No se puede mover una carpeta dentro de sí misma.' }
            $target = Join-Path $dest (Split-Path -Leaf $src)
            if ($target -ieq $src) { Send-Json $ctx 200 @{ path = (To-Rel $src) }; return }
            if (Test-Path -LiteralPath $target) { Fail 409 'En el destino ya existe un elemento con ese nombre.' }
            if ($isFile) { [IO.File]::Move($src, $target) } else { [IO.Directory]::Move($src, $target) }
            try { if (-not $isFile) { Move-FolderMeta (To-Rel $src) (To-Rel $target) } }
            catch { if (-not $isFile) { [IO.Directory]::Move($target, $src) }; throw }
            Send-Json $ctx 200 @{ path = (To-Rel $target) }
            return
        }

        'POST /api/delete' {
            $b = Read-JsonBody $req
            $full = Resolve-Rel $b.path
            Assert-Managed $full
            $rel = To-Rel $full
            $stamp = (Get-Date).ToString('yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N')
            $trash = Join-Path (Join-Path $Root '.papelera') $stamp
            $dest = Join-Path $trash ($rel.Replace('/', '\'))
            Assert-NoReparse $dest
            [void][IO.Directory]::CreateDirectory((Split-Path -Parent $dest))
            if (Test-Path -LiteralPath $full -PathType Leaf) { [IO.File]::Move($full, $dest) } else { [IO.Directory]::Move($full, $dest) }
            try { Move-FolderMeta $rel '' }
            catch { if ([IO.File]::Exists($dest)) { [IO.File]::Move($dest, $full) } else { [IO.Directory]::Move($dest, $full) }; throw }
            Send-Json $ctx 200 @{ trashed = ".papelera/$stamp/$rel" }
            return
        }

        'POST /api/upload' {
            $dir = Resolve-Rel $q['dir'] $true
            if (-not (Test-Path -LiteralPath $dir -PathType Container)) { Fail 404 'La carpeta destino no existe.' }
            $name = [string]$q['name']
            Assert-Name $name $true
            $bytes = Read-Body $req $MaxFileUploadBytes
            $final = Get-UniqueName $dir $name
            [IO.File]::WriteAllBytes((Join-Path $dir $final), $bytes)
            Send-Json $ctx 200 @{ path = (To-Rel (Join-Path $dir $final)); name = $final }
            return
        }

        'GET /api/zip' {
            $full = Resolve-Rel $q['path'] $true
            if (-not (Test-Path -LiteralPath $full -PathType Container)) { Fail 404 'La carpeta no existe.' }
            $folderName = if ($full -ieq $Root) { 'Noera' } else { Split-Path -Leaf $full }
            $zipName = "$folderName.zip"

            $tmpZip = Join-Path $AppDir ("download_" + [Guid]::NewGuid().ToString('N') + '.zip')
            try { New-FolderZip $full $tmpZip; Send-File $ctx $tmpZip 'application/zip' $zipName }
            finally { if ([IO.File]::Exists($tmpZip)) { [IO.File]::Delete($tmpZip) } }
            return
        }

        'GET /api/noera/zip' {
            $tmpZip = Join-Path $AppDir ("source_" + [Guid]::NewGuid().ToString('N') + '.zip')
            $output = $null; $zip = $null
            try {
                $output = [IO.File]::Open($tmpZip, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
                $zip = New-Object IO.Compression.ZipArchive($output, [IO.Compression.ZipArchiveMode]::Create, $true)
                # Lista explícita: no exportar temporales de subidas o extracciones.
                $paths = @('iniciar-noera.bat', '_LEEME.md', '_REVISION.md', '_app/server.ps1', '_app/app.js', '_app/app.css', '_app/index.html', '_app/metadata.json', '_app/changelog.json', '_tests/backend.Tests.ps1', '_tests/frontend.Tests.cjs')
                foreach ($rel in $paths) {
                    $full = Join-Path $Root ($rel.Replace('/', '\'))
                    Assert-NoReparse $full
                    if (-not [IO.File]::Exists($full)) { continue }
                    $entry = $zip.CreateEntry($rel, [IO.Compression.CompressionLevel]::Optimal)
                    $stream = $entry.Open(); $inputFile = $null
                    try { $inputFile = [IO.File]::OpenRead($full); $inputFile.CopyTo($stream) }
                    finally { if ($inputFile) { $inputFile.Dispose() }; $stream.Dispose() }
                }
                $zip.Dispose(); $zip = $null
                $output.Dispose(); $output = $null
                Send-File $ctx $tmpZip 'application/zip' 'Noera-Software-Source.zip'
            } finally {
                if ($zip) { $zip.Dispose() }; if ($output) { $output.Dispose() }
                if ([IO.File]::Exists($tmpZip)) { [IO.File]::Delete($tmpZip) }
            }
            return
        }

        'GET /api/noera/files' {
            $coreFiles = @(
                @{ path = '_app/server.ps1'; full = (Join-Path $AppDir 'server.ps1'); lang = 'powershell' },
                @{ path = '_app/app.js'; full = (Join-Path $AppDir 'app.js'); lang = 'javascript' },
                @{ path = '_app/app.css'; full = (Join-Path $AppDir 'app.css'); lang = 'css' },
                @{ path = '_app/index.html'; full = (Join-Path $AppDir 'index.html'); lang = 'html' },
                @{ path = 'iniciar-noera.bat'; full = (Join-Path $Root 'iniciar-noera.bat'); lang = 'bat' }
            )
            $list = @()
            foreach ($c in $coreFiles) {
                if (Test-Path -LiteralPath $c.full) {
                    $fi = Get-Item -LiteralPath $c.full
                    $bytes = [IO.File]::ReadAllBytes($c.full)
                    $text = $Utf8Strict.GetString($bytes)
                    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { $text = $text.Substring(1) }
                    $list += @{
                        name = $fi.Name
                        path = $c.path
                        lang = $c.lang
                        size = $fi.Length
                        mtime = $fi.LastWriteTimeUtc.Ticks.ToString()
                        content = $text
                    }
                }
            }
            Send-Json $ctx 200 @{ files = $list }
            return
        }

        'GET /api/noera/changelog' {
            $clFile = Join-Path $AppDir 'changelog.json'
            if (Test-Path -LiteralPath $clFile) {
                $json = [IO.File]::ReadAllText($clFile, [Text.Encoding]::UTF8)
                Send-Bytes $ctx 200 'application/json; charset=utf-8' ([Text.Encoding]::UTF8.GetBytes($json))
            } else {
                Send-Json $ctx 200 @()
            }
            return
        }

        'POST /api/noera/update-zip' {
            $uploadedName = [string]$q['name']
            $allowedNames = @('Noera-Software-Source.zip', 'Noera.zip')
            if ($allowedNames -notcontains $uploadedName) {
                Fail 400 "Nombre de archivo inválido. El archivo debe llamarse exactamente 'Noera-Software-Source.zip' (o 'Noera.zip'). Recibido: '$uploadedName'."
            }

            $bytes = Read-Body $req $MaxUploadBytes
            if ($bytes.Length -lt 22) { Fail 400 'El archivo recibido está vacío o no es un ZIP válido.' }

            $id = (Get-Date).ToString('yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N')
            $tempZip = Join-Path $AppDir ("up_noera_$id.zip")
            $tempExtract = Join-Path $AppDir ("extract_noera_$id")
            $historyDir = Join-Path (Join-Path $Root '.history') '_noera'
            Assert-NoReparse $historyDir
            [void][IO.Directory]::CreateDirectory($historyDir)
            $backupZipFile = "backup_${id}_Noera-Software-Source.zip"
            $backupZipPath = Join-Path $historyDir $backupZipFile

            try {
                [IO.File]::WriteAllBytes($tempZip, $bytes)
                [void][IO.Directory]::CreateDirectory($tempExtract)
                $entryCount = Expand-ValidatedZip $tempZip $tempExtract

                # Si el ZIP contiene _app/ o si contiene los archivos directamente
                $extractedAppDir = Join-Path $tempExtract '_app'
                $extractedBat = Join-Path $tempExtract 'iniciar-noera.bat'

                if (-not [IO.Directory]::Exists($extractedAppDir)) {
                    $firstLevelDirs = @(Get-ChildItem -LiteralPath $tempExtract -Directory -Force -ErrorAction Stop)
                    if ($firstLevelDirs.Count -eq 1 -and [IO.Directory]::Exists((Join-Path $firstLevelDirs[0].FullName '_app'))) {
                        $extractedAppDir = Join-Path $firstLevelDirs[0].FullName '_app'
                        $extractedBat = Join-Path $firstLevelDirs[0].FullName 'iniciar-noera.bat'
                    }
                    elseif ([IO.File]::Exists((Join-Path $tempExtract 'server.ps1'))) {
                        $extractedAppDir = $tempExtract
                    }
                }

                if (-not [IO.Directory]::Exists($extractedAppDir)) {
                    Fail 400 'El ZIP no contiene una estructura válida de Noera (no se encontró carpeta _app ni server.ps1).'
                }

                # Backup previo de Noera actual
                $ms = New-Object IO.MemoryStream
                $oldZip = New-Object IO.Compression.ZipArchive($ms, [IO.Compression.ZipArchiveMode]::Create, $true)

                $batFile = Join-Path $Root 'iniciar-noera.bat'
                if ([IO.File]::Exists($batFile)) {
                    $entry = $oldZip.CreateEntry('iniciar-noera.bat', [IO.Compression.CompressionLevel]::Optimal)
                    $stream = $entry.Open()
                    $b = [IO.File]::ReadAllBytes($batFile)
                    $stream.Write($b, 0, $b.Length)
                    $stream.Close()
                }

                $appFiles = Get-ChildItem -LiteralPath $AppDir -File -Force -ErrorAction SilentlyContinue
                foreach ($f in $appFiles) {
                    $entry = $oldZip.CreateEntry("_app/$($f.Name)", [IO.Compression.CompressionLevel]::Optimal)
                    $stream = $entry.Open()
                    $b = [IO.File]::ReadAllBytes($f.FullName)
                    $stream.Write($b, 0, $b.Length)
                    $stream.Close()
                }

                $oldZip.Dispose()
                $backupBytes = $ms.ToArray()
                $ms.Dispose()
                [IO.File]::WriteAllBytes($backupZipPath, $backupBytes)
                $backupSize = $backupBytes.Length

                # Copiar lanzador si está presente
                if ([IO.File]::Exists($extractedBat)) {
                    Copy-Item -LiteralPath $extractedBat -Destination (Join-Path $Root 'iniciar-noera.bat') -Force
                }

                # Copiar archivos a _app (sobrescribir)
                $newAppFiles = Get-ChildItem -LiteralPath $extractedAppDir -File -Force
                foreach ($nf in $newAppFiles) {
                    if ($nf.Name -ieq 'metadata.json' -and [IO.File]::Exists((Join-Path $AppDir 'metadata.json'))) {
                        continue
                    }
                    Copy-Item -LiteralPath $nf.FullName -Destination (Join-Path $AppDir $nf.Name) -Force
                }

                # Copiar tests y documentación si vienen en el ZIP
                $extractedLeeme = Join-Path $tempExtract '_LEEME.md'
                if ([IO.File]::Exists($extractedLeeme)) { Copy-Item -LiteralPath $extractedLeeme -Destination (Join-Path $Root '_LEEME.md') -Force }
                $extractedRev = Join-Path $tempExtract '_REVISION.md'
                if ([IO.File]::Exists($extractedRev)) { Copy-Item -LiteralPath $extractedRev -Destination (Join-Path $Root '_REVISION.md') -Force }
                $extractedTests = Join-Path $tempExtract '_tests'
                if ([IO.Directory]::Exists($extractedTests)) {
                    $targetTests = Join-Path $Root '_tests'
                    [void][IO.Directory]::CreateDirectory($targetTests)
                    Copy-Item -LiteralPath (Join-Path $extractedTests '*') -Destination $targetTests -Recurse -Force
                }

                # Registrar en metadata
                $meta = Get-NoeraMeta
                if (-not $meta.taggedFolders) {
                    $meta | Add-Member -MemberType NoteProperty -Name 'taggedFolders' -Value ([PSCustomObject]@{})
                }
                if (-not $meta.taggedFolders.PSObject.Properties['_noera']) {
                    $meta.taggedFolders | Add-Member -MemberType NoteProperty -Name '_noera' -Value ([PSCustomObject]@{
                        update = $true
                        taggedAt = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
                        history = @()
                    })
                }
                $historyRecord = [PSCustomObject]@{
                    id = $id
                    date = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
                    zipName = $uploadedName
                    backupRel = ".history/_noera/$backupZipFile"
                    backupSize = $backupSize
                    newSize = $bytes.Length
                    entries = $entryCount
                }
                $meta.taggedFolders._noera.history = @($historyRecord) + @($meta.taggedFolders._noera.history)
                Save-NoeraMeta $meta

                Send-Json $ctx 200 @{
                    ok = $true
                    target = '_noera'
                    zipName = $uploadedName
                    history = $historyRecord
                    meta = $meta
                }
            }
            finally {
                if ([IO.Directory]::Exists($tempExtract)) { Remove-Item -LiteralPath $tempExtract -Recurse -Force -ErrorAction SilentlyContinue }
                if ([IO.File]::Exists($tempZip)) { [IO.File]::Delete($tempZip) }
            }
            return
        }

        'GET /api/folder/meta' {
            $meta = Get-NoeraMeta
            Send-Json $ctx 200 $meta
            return
        }

        'POST /api/folder/tag' {
            $b = Read-JsonBody $req
            $relPath = [string]$b.path
            $full = Resolve-Rel $relPath $false
            $relPath = To-Rel $full
            if (-not (Test-Path -LiteralPath $full -PathType Container)) { Fail 404 'La carpeta no existe.' }
            $meta = Get-NoeraMeta
            if (-not $meta.taggedFolders) {
                $meta | Add-Member -MemberType NoteProperty -Name 'taggedFolders' -Value ([PSCustomObject]@{})
            }
            $enabled = [bool]$b.enabled
            if ($enabled) {
                if ($meta.taggedFolders.PSObject.Properties[$relPath]) {
                    $meta.taggedFolders.$relPath.update = $true
                } else {
                    $meta.taggedFolders | Add-Member -MemberType NoteProperty -Name $relPath -Value ([PSCustomObject]@{
                        update = $true
                        taggedAt = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
                        history = @()
                    })
                }
            } else {
                if ($meta.taggedFolders.PSObject.Properties[$relPath]) {
                    $meta.taggedFolders.$relPath.update = $false
                }
            }
            Save-NoeraMeta $meta
            Send-Json $ctx 200 @{ path = $relPath; update = $enabled; meta = $meta }
            return
        }

        'POST /api/folder/update-zip' {
            $full = Resolve-Rel ([string]$q['path']) $false
            $relPath = To-Rel $full
            if (-not [IO.Directory]::Exists($full)) { Fail 404 'La carpeta no existe.' }
            $folderName = Split-Path -Leaf $full
            $expectedZip = "$folderName.zip"
            if ([string]$q['name'] -ine $expectedZip) { Fail 400 "El ZIP debe llamarse '$expectedZip'." }
            $bytes = Read-Body $req $MaxUploadBytes
            if ($bytes.Length -lt 22) { Fail 400 'El archivo no es un ZIP válido.' }
            $id = (Get-Date).ToString('yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N')
            $tempZip = Join-Path $AppDir ("upload_$id.zip")
            $tempExtract = Join-Path $AppDir ("extract_$id")
            $historyDir = Join-Path (Join-Path $Root '.history') ($relPath.Replace('/', '\'))
            Assert-NoReparse $historyDir
            [void][IO.Directory]::CreateDirectory($historyDir)
            $backupZipFile = "backup_${id}_${expectedZip}"
            $backupZipPath = Join-Path $historyDir $backupZipFile
            # Se conserva el directorio original hasta confirmar también los metadatos.
            $rollback = Join-Path $historyDir ("original_$id")
            $swapped = $false; $committed = $false
            try {
                [IO.File]::WriteAllBytes($tempZip, $bytes)
                [void][IO.Directory]::CreateDirectory($tempExtract)
                $entryCount = Expand-ValidatedZip $tempZip $tempExtract
                $extractedItems = @(Get-ChildItem -LiteralPath $tempExtract -Force -ErrorAction Stop)
                $sourceDir = $tempExtract
                if ($extractedItems.Count -eq 1 -and $extractedItems[0].PSIsContainer -and $extractedItems[0].Name -ieq $folderName) { $sourceDir = $extractedItems[0].FullName }
                # Backup completo: incluye binarios, recursos, carpetas vacías y archivos ocultos.
                New-FolderZip $full $backupZipPath
                $backupSize = (Get-Item -LiteralPath $backupZipPath).Length
                $meta = Get-NoeraMeta
                if (-not $meta.taggedFolders.PSObject.Properties[$relPath]) {
                    $meta.taggedFolders | Add-Member -MemberType NoteProperty -Name $relPath -Value ([PSCustomObject]@{ update = $true; taggedAt = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'); history = @() })
                }
                $record = [PSCustomObject]@{ id = $id; date = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'); zipName = $expectedZip; backupRel = ".history/$relPath/$backupZipFile"; backupSize = $backupSize; newSize = $bytes.Length; entries = $entryCount }
                $meta.taggedFolders.$relPath.history = @($record) + @($meta.taggedFolders.$relPath.history)
                [IO.Directory]::Move($full, $rollback)
                try { [IO.Directory]::Move($sourceDir, $full); $swapped = $true }
                catch { [IO.Directory]::Move($rollback, $full); throw }
                Save-NoeraMeta $meta
                $committed = $true
                Send-Json $ctx 200 @{ ok = $true; path = $relPath; zipName = $expectedZip; history = $record; meta = $meta }
            }
            catch {
                if ($swapped -and -not $committed) {
                    # Se aparta la versión nueva antes de recuperar el original intacto.
                    $failed = Join-Path $AppDir ("failed_$id")
                    [IO.Directory]::Move($full, $failed)
                    [IO.Directory]::Move($rollback, $full)
                    Remove-Item -LiteralPath $failed -Recurse -Force -ErrorAction SilentlyContinue
                }
                throw
            }
            finally {
                if ($committed -and [IO.Directory]::Exists($rollback)) { Remove-Item -LiteralPath $rollback -Recurse -Force -ErrorAction SilentlyContinue }
                if ([IO.Directory]::Exists($tempExtract)) { Remove-Item -LiteralPath $tempExtract -Recurse -Force -ErrorAction SilentlyContinue }
                if ([IO.File]::Exists($tempZip)) { [IO.File]::Delete($tempZip) }
            }
            return
        }

        'GET /api/folder/history/download' {
            $relFile = [string]$q['file']
            $relFile = $relFile.Replace('/', '\').Trim('\')
            if (-not $relFile.StartsWith('.history\')) { Fail 403 'Acceso no permitido.' }
            $full = [IO.Path]::GetFullPath((Join-Path $Root $relFile))
            if (-not $full.StartsWith($Root + '\.history\', [StringComparison]::OrdinalIgnoreCase)) { Fail 403 'Ruta fuera de historial.' }
            if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { Fail 404 'Archivo de respaldo no encontrado.' }
            Assert-NoReparse $full
            if ([IO.Path]::GetExtension($full) -ine '.zip') { Fail 403 'Solo se descargan respaldos ZIP.' }
            Send-File $ctx $full 'application/zip' (Split-Path -Leaf $full)
            return
        }

        default { Fail 404 'Endpoint no encontrado.' }
    }
}

# ---------- arranque ----------
$listener = $null
for ($p = $Port; $p -lt ($Port + 10); $p++) {
    $l = New-Object System.Net.HttpListener
    $l.Prefixes.Add("http://127.0.0.1:$p/")
    try { $l.Start(); $listener = $l; $Port = $p; break } catch { $l.Close() }
}
if (-not $listener) { Write-Host "No se pudo abrir ningún puerto entre $Port y $($Port + 9)." -ForegroundColor Red; exit 1 }

$url = "http://127.0.0.1:$Port/"
Write-Host ""
Write-Host "  NOERA - Central de archivos" -ForegroundColor Yellow
Write-Host "  Carpeta : $Root"
Write-Host "  Panel   : $url"
Write-Host "  Detener : Ctrl+C o cerrar esta ventana"
Write-Host ""
if (-not $NoBrowser) { Start-Process $url }

try {
    while ($listener.IsListening) {
        $task = $listener.GetContextAsync()
        while (-not $task.AsyncWaitHandle.WaitOne(300)) { }
        $ctx = $task.Result
        try { Handle $ctx }
        catch {
            $m = $_.Exception.Message
            $code = 500
            if ($m -like 'API|*') { $parts = $m.Split('|', 3); $code = [int]$parts[1]; $msg = $parts[2] }
            else { $msg = 'Error interno del servidor.'; Write-Host "[error] $m" -ForegroundColor Red }
            try { Send-Json $ctx $code @{ error = $msg } } catch { try { $ctx.Response.Abort() } catch { } }
        }
    }
}
finally { $listener.Stop(); $listener.Close() }
