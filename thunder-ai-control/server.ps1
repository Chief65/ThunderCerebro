param(
    [int]$Port = 4848
)

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path -Parent $scriptDir
$publicDir = Join-Path $scriptDir "public"

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "    BEACON // THUNDER CEREBRO CONTROL CENTER" -ForegroundColor Cyan
Write-Host "    Servidor Local de Control y Lanzador Antigravity" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "  Workspace: $workspaceRoot" -ForegroundColor DarkCyan
Write-Host "  Puerto:    $Port" -ForegroundColor DarkCyan
Write-Host "  Web UI:    http://localhost:$Port" -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor Yellow

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")

try {
    $listener.Start()
} catch {
    Write-Error "No se pudo iniciar el listener en http://localhost:$Port/. ¿Ya está en uso?"
    exit 1
}

function Get-ContentType {
    param([string]$path)
    $ext = [System.IO.Path]::GetExtension($path).ToLower()
    switch ($ext) {
        ".html" { return "text/html; charset=utf-8" }
        ".css"  { return "text/css; charset=utf-8" }
        ".js"   { return "application/javascript; charset=utf-8" }
        ".json" { return "application/json; charset=utf-8" }
        ".png"  { return "image/png" }
        ".ico"  { return "image/x-icon" }
        default { return "text/plain; charset=utf-8" }
    }
}

function Send-Response {
    param(
        [System.Net.HttpListenerResponse]$Response,
        [string]$Content,
        [string]$ContentType = "application/json; charset=utf-8",
        [int]$StatusCode = 200
    )
    $buffer = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $Response.StatusCode = $StatusCode
    $Response.ContentType = $ContentType
    $Response.ContentLength64 = $buffer.Length
    $Response.AddHeader("Access-Control-Allow-Origin", "*")
    $Response.AddHeader("Access-Control-Allow-Headers", "Content-Type")
    $Response.AddHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    $Response.OutputStream.Write($buffer, 0, $buffer.Length)
    $Response.OutputStream.Close()
}

function Send-File {
    param(
        [System.Net.HttpListenerResponse]$Response,
        [string]$FilePath
    )
    if (Test-Path $FilePath) {
        $bytes = [System.IO.File]::ReadAllBytes($FilePath)
        $Response.StatusCode = 200
        $Response.ContentType = Get-ContentType $FilePath
        $Response.ContentLength64 = $bytes.Length
        $Response.AddHeader("Access-Control-Allow-Origin", "*")
        $Response.OutputStream.Write($bytes, 0, $bytes.Length)
        $Response.OutputStream.Close()
    } else {
        Send-Response -Response $Response -Content '{"error": "Archivo no encontrado"}' -StatusCode 404
    }
}

function Get-SkillsData {
    $skills = @()
    $skillDirs = @(
        (Join-Path $workspaceRoot "skills"),
        (Join-Path $workspaceRoot ".agents\skills")
    )
    
    $seen = @{}
    foreach ($dir in $skillDirs) {
        if (-not (Test-Path $dir)) { continue }
        $files = Get-ChildItem -Path $dir -Recurse -Filter "*.md"
        foreach ($f in $files) {
            $name = $f.BaseName
            if ($name -eq "SKILL" -or $name -eq "README") {
                $name = $f.Directory.Name
            }
            if ($seen.ContainsKey($name)) { continue }
            $seen[$name] = $true
            
            $text = [System.IO.File]::ReadAllText($f.FullName)
            $desc = ""
            if ($text -match "(?s)description:\s*>?-?\s*(.*?)(?:\n---|\n[a-z_]+:)") {
                $desc = $matches[1].Trim() -replace "\s+", " "
            } elseif ($text -match "(?m)^# (.*)") {
                $desc = $matches[1].Trim()
            }
            
            # Determine domain category
            $cat = "General"
            $lower = "$name $desc $($f.FullName)".ToLower()
            if ($lower -match "deluxemenus|minecraft|survival|spawner|mob|boss|rpg|itemedit|plan|server") {
                $cat = "Minecraft & Red"
            } elseif ($lower -match "obsidian|vault|cerebro|nota|inbox") {
                $cat = "Obsidian & Cerebro"
            } elseif ($lower -match "studio|lore|dialogue|narrative|character|guion") {
                $cat = "ThunderStudios"
            } elseif ($lower -match "monetizacion|mercado|producto|negocio|decisiones") {
                $cat = "Estrategia & Negocio"
            }
            
            $skills += [PSCustomObject]@{
                id = $name
                name = $name
                category = $cat
                description = $desc
                file = $f.FullName.Substring($workspaceRoot.Length + 1).Replace('\', '/')
            }
        }
    }
    return $skills
}

function Get-SubagentsData {
    $subagents = @(
        [PSCustomObject]@{
            id = "self"
            name = "Self / Beacon Core"
            type = "Core"
            role = "Agente Principal Autónomo"
            description = "Hereda la configuración completa del sistema, herramientas de lectura/escritura, terminal y modelos."
            domain = "Sistema"
        },
        [PSCustomObject]@{
            id = "research"
            name = "Codebase Researcher"
            type = "Research"
            role = "Investigador de Repositorio"
            description = "Explora el código, busca en la web y extrae documentación técnica de forma no destructiva."
            domain = "Ingeniería"
        },
        [PSCustomObject]@{
            id = "narrative-architect"
            name = "Narrative Architect"
            type = "ThunderStudios"
            role = "Arquitecto de Lore & Estructura"
            description = "Estructura arcos argumentales de varias temporadas, mitología y cánones del THUNDERVERSE."
            domain = "Estudio"
        },
        [PSCustomObject]@{
            id = "lore-keeper"
            name = "Lore Keeper"
            type = "ThunderStudios"
            role = "Guardián de Continuidad y Reglas"
            description = "Garantiza la consistencia canónica y la lógica interna de todas las ramas narrativas."
            domain = "Estudio"
        },
        [PSCustomObject]@{
            id = "character-designer"
            name = "Character Designer"
            type = "ThunderStudios"
            role = "Diseñador de Personajes y Arquetipos"
            description = "Define perfiles psicológicos, motivaciones y evolución de entidades y héroes."
            domain = "Estudio"
        },
        [PSCustomObject]@{
            id = "dialogue-writer"
            name = "Dialogue Writer"
            type = "ThunderStudios"
            role = "Escritor de Diálogos & Voces"
            description = "Redacta parlamentos, interacciones de NPCs (FancyNpcs) y guiones cinematográficos."
            domain = "Estudio"
        },
        [PSCustomObject]@{
            id = "deluxemenus-builder"
            name = "DeluxeMenus Builder"
            type = "Minecraft"
            role = "Especialista en GUI & DeluxeMenus"
            description = "Diseña y optimiza configuraciones de inventarios YAML con paletas estandarizadas."
            domain = "Minecraft"
        }
    )
    return $subagents
}

function Get-GraphData {
    $wikiDir = Join-Path $workspaceRoot "wiki"
    $files = Get-ChildItem -Path $wikiDir -Recurse -Filter "*.md"
    
    $nodes = @()
    $nodeMap = @{}
    $linkList = @()
    
    foreach ($f in $files) {
        $rel = $f.FullName.Substring($workspaceRoot.Length + 1).Replace('\', '/')
        $id = $f.BaseName
        $cat = "General"
        
        if ($rel -match "core-infrastructure") { $cat = "Core" }
        elseif ($rel -match "economy-progression") { $cat = "Economía" }
        elseif ($rel -match "gameplay-mechanics") { $cat = "Gameplay & RPG" }
        elseif ($rel -match "world-protection") { $cat = "Protección" }
        elseif ($rel -match "chat-social") { $cat = "Social & Chat" }
        elseif ($rel -match "concepts") { $cat = "Conceptos" }
        elseif ($rel -match "synthesis") { $cat = "Síntesis" }
        elseif ($rel -match "sources") { $cat = "Fuentes" }
        
        $nodeObj = [PSCustomObject]@{
            id = $id
            label = $id
            file = $rel
            category = $cat
            inDegree = 0
            outDegree = 0
        }
        $nodes += $nodeObj
        $nodeMap[$id] = $nodeObj
    }
    
    # Second pass: scan wikilinks
    $regex = [regex]'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]'
    foreach ($f in $files) {
        $sourceId = $f.BaseName
        $text = [System.IO.File]::ReadAllText($f.FullName)
        $matches = $regex.Matches($text)
        
        $seenTarget = @{}
        foreach ($m in $matches) {
            $raw = $m.Groups[1].Value.Trim()
            $targetBase = [System.IO.Path]::GetFileNameWithoutExtension($raw)
            
            if ($nodeMap.ContainsKey($targetBase) -and $targetBase -ne $sourceId -and -not $seenTarget.ContainsKey($targetBase)) {
                $seenTarget[$targetBase] = $true
                $linkList += [PSCustomObject]@{
                    source = $sourceId
                    target = $targetBase
                }
                $nodeMap[$sourceId].outDegree++
                $nodeMap[$targetBase].inDegree++
            }
        }
    }
    
    return [PSCustomObject]@{
        nodes = $nodes
        links = $linkList
        stats = [PSCustomObject]@{
            totalNodes = $nodes.Count
            totalLinks = $linkList.Count
        }
    }
}

function Get-RecentLogs {
    $logPath = Join-Path $workspaceRoot "log.md"
    $entries = @()
    if (Test-Path $logPath) {
        $text = [System.IO.File]::ReadAllText($logPath)
        $blocks = $text -split "(?m)^## \["
        foreach ($b in $blocks) {
            if ($b -match "^(\d{4}-\d{2}-\d{2})\]\s*(.*?)\s*\|\s*(.*?)\r?\n(.*)") {
                $entries += [PSCustomObject]@{
                    date = $matches[1]
                    tag = $matches[2]
                    title = $matches[3]
                    body = $matches[4].Trim()
                }
            }
            if ($entries.Count -ge 15) { break }
        }
    }
    return $entries
}

function Launch-AntigravitySession {
    param([hashtable]$Data)
    
    $topic = $Data["topic"]
    $model = $Data["model"]
    $effort = $Data["effort"]
    $mode = $Data["mode"]
    $customPrompt = $Data["prompt"]
    
    # Build agy command line
    $agyCmd = "agy --dangerously-skip-permissions"
    
    if ($model) {
        $agyCmd += " --model $model"
    }
    if ($effort) {
        $agyCmd += " --effort $effort"
    }
    if ($mode -eq "plan") {
        $agyCmd += " --mode plan"
    }
    
    # If initial prompt is supplied
    $initPrompt = ""
    if ($customPrompt -and $customPrompt.Trim()) {
        $initPrompt = $customPrompt.Trim()
    } elseif ($topic) {
        switch ($topic) {
            "minecraft" { $initPrompt = "Hola Beacon. Iniciamos sesión de trabajo en ThunderMC Survival (Minecraft 1.21.11). Analicemos el estado de plugins y balance económico." }
            "obsidian"  { $initPrompt = "Hola Beacon. Iniciamos sesión de gestión de conocimiento en Obsidian (ThunderCerebro). Revisemos notas y grafo." }
            "studio"    { $initPrompt = "Hola Beacon. Iniciamos sesión creativa de ThunderStudios para desarrollo del THUNDERVERSE." }
            "negocio"   { $initPrompt = "Hola Beacon. Iniciamos sesión de monetización, estudio de mercado y tienda Tebex de ThunderMC." }
            "dev"       { $initPrompt = "Hola Beacon. Iniciamos sesión técnica de arquitectura y desarrollo de plugins/automatizaciones." }
            default     { $initPrompt = "Hola Beacon. ¿En qué trabajamos hoy?" }
        }
    }
    
    if ($initPrompt) {
        $safePrompt = $initPrompt.Replace('"', '\"')
        $agyCmd += " -i `"$safePrompt`""
    }
    
    # Check Windows Terminal
    $wtPath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\wt.exe"
    $hasWt = Test-Path $wtPath
    
    if ($hasWt) {
        $procArgs = "-d `"$workspaceRoot`" --title `"Beacon // ThunderCerebro`" powershell -NoExit -Command `"Write-Host '=====================================================' -ForegroundColor Yellow; Write-Host '  SESION BEACON (THUNDER CEREBRO) ACTIVA' -ForegroundColor Cyan; Write-Host '=====================================================' -ForegroundColor Yellow; Write-Host 'Ejecutando: $agyCmd' -ForegroundColor DarkGray; $agyCmd`""
        Start-Process $wtPath -ArgumentList $procArgs
    } else {
        $procArgs = "-NoExit -Command `"Set-Location '$workspaceRoot'; Write-Host '=====================================================' -ForegroundColor Yellow; Write-Host '  SESION BEACON (THUNDER CEREBRO) ACTIVA' -ForegroundColor Cyan; Write-Host '=====================================================' -ForegroundColor Yellow; $agyCmd`""
        Start-Process powershell.exe -ArgumentList $procArgs
    }
    
    return [PSCustomObject]@{
        success = $true
        command = $agyCmd
        launcher = if ($hasWt) { "Windows Terminal" } else { "PowerShell" }
    }
}

# ==========================================================
# Session Telemetry & Real-Time Token Tracking
# ==========================================================
$global:SessionTelemetry = [PSCustomObject]@{
    Messages = [System.Collections.ArrayList]::new()
    TotalTokens = 1500
    InputTokens = 1500
    OutputTokens = 0
    ActiveModel = "gemini-3.8-flash"
}

function Get-ModelMaxContext {
    param([string]$model)
    if ($model -like "*pro*") {
        return 2097152
    } elseif ($model -like "*sonnet*") {
        return 200000
    } else {
        return 1048576
    }
}

function Get-PerformanceReport {
    $activeModel = $global:SessionTelemetry.ActiveModel
    $maxContext = Get-ModelMaxContext -model $activeModel
    $totalTok = [math]::Max(1500, $global:SessionTelemetry.TotalTokens)
    $pct = [math]::Round(($totalTok / $maxContext) * 100, 2)
    if ($pct -eq 0 -and $totalTok -gt 0) {
        $pct = [math]::Round(($totalTok / $maxContext) * 100, 3)
    }

    # Scan heavy files
    $heavyFiles = @()
    try {
        $candidateFiles = Get-ChildItem -Path $workspaceRoot -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object { 
                $_.FullName -notmatch '\\\.git\\' -and 
                $_.FullName -notmatch '\\\.obsidian\\' -and
                $_.FullName -notmatch '\\node_modules\\' -and
                $_.Extension -match '\.(md|yml|yaml|json|txt|log|sparkprofile|sql|conf|properties)$'
            } |
            Sort-Object Length -Descending |
            Select-Object -First 10

        foreach ($f in $candidateFiles) {
            $relPath = $f.FullName.Substring($workspaceRoot.Length + 1).Replace('\', '/')
            $approxTokens = [math]::Round($f.Length / 4)
            $risk = "Bajo"
            if ($f.Length -gt 10MB) {
                $risk = "Peligro Crítico"
            } elseif ($f.Length -gt 250KB -or $approxTokens -gt 60000) {
                $risk = "Alto Consumo"
            } elseif ($approxTokens -gt 15000) {
                $risk = "Moderado"
            }

            $heavyFiles += [PSCustomObject]@{
                name = $f.Name
                path = $relPath
                sizeKB = [math]::Round($f.Length / 1KB, 1)
                tokens = $approxTokens
                risk = $risk
            }
        }
    } catch {
        Write-Warning "Error escaneando archivos: $_"
    }

    # Process breakdown estimation
    $bFiles = 42
    $bHist = if ($global:SessionTelemetry.Messages.Count -gt 4) { 28 } else { 15 }
    $bShell = 16
    $bOutput = if ($global:SessionTelemetry.OutputTokens -gt 0) { 15 } else { 8 }
    $bSys = [math]::Max(5, 100 - ($bFiles + $bHist + $bShell + $bOutput))

    $recommendations = @(
        [PSCustomObject]@{
            title = "Peligro de Lectura Total en log.md y Bases de Datos"
            description = "Archivos como log.md (42k tokens) o server-database.yml (96k tokens) saturan la ventana si se leen íntegros. Utilice lecturas por corte con StartLine y EndLine."
            severity = "Alta"
            icon = "⚠️"
        },
        [PSCustomObject]@{
            title = "Exclusión Inmediata de Volcados Binarios (.sparkprofile)"
            description = "Existen volcados Spark de hasta 44 MB (~11 Millones de tokens) en raw/. Bloquee explícitamente su ingesta directa a la IA para evitar desbordamiento."
            severity = "Crítica"
            icon = "🛑"
        },
        [PSCustomObject]@{
            title = "Segmentación Atómica en Obsidian (Wiki)"
            description = "Mantenga notas de conceptos por debajo de 150 líneas. Esto permite responder consultas técnicas precisas sin arrastrar texto sobrante al prompt."
            severity = "Media"
            icon = "💡"
        },
        [PSCustomObject]@{
            title = "Purgar Contexto antes del 40% de Ocupación"
            description = "Al superar el 40% de la ventana de contexto, el modelo experimenta degradación de atención y latencia incrementada. Limpie el chat periódicamente."
            severity = "Recomendado"
            icon = "🧹"
        }
    )

    return [PSCustomObject]@{
        activeModel = $activeModel
        maxContext = $maxContext
        totalTokens = $totalTok
        inputTokens = $global:SessionTelemetry.InputTokens
        outputTokens = $global:SessionTelemetry.OutputTokens
        usagePercent = $pct
        breakdown = [PSCustomObject]@{
            files = $bFiles
            history = $bHist
            shell = $bShell
            output = $bOutput
            system = $bSys
        }
        heavyFiles = $heavyFiles
        recommendations = $recommendations
        messagesCount = $global:SessionTelemetry.Messages.Count
    }
}

function Invoke-BeaconChat {
    param(
        [string]$Message,
        [string]$Model
    )

    if ($Model -and $Model.Trim()) {
        $global:SessionTelemetry.ActiveModel = $Model.Trim()
    }
    $activeModel = $global:SessionTelemetry.ActiveModel
    $maxContext = Get-ModelMaxContext -model $activeModel

    $turnInput = [math]::Ceiling($Message.Length / 4) + 20
    $prevHistoryTokens = [math]::Min(50000, $global:SessionTelemetry.Messages.Count * 250)
    $effectiveInput = $turnInput + $prevHistoryTokens + 1500

    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $replyText = ""

    try {
        $hasAgy = [bool](Get-Command "agy" -ErrorAction SilentlyContinue)
        if (-not $hasAgy) {
            $hasAgy = [bool](Get-Command "agy.cmd" -ErrorAction SilentlyContinue)
        }

        if ($hasAgy) {
            if ($activeModel -and $activeModel -ne "default") {
                $replyText = & agy --dangerously-skip-permissions -p $Message --model $activeModel --effort high 2>&1 | Out-String
            } else {
                $replyText = & agy --dangerously-skip-permissions -p $Message 2>&1 | Out-String
            }
        } else {
            $replyText = "Sr Ramos, el ejecutable de Antigravity ('agy') no se encuentra en el PATH del sistema."
        }
    }
    catch {
        $replyText = "Sr Ramos, ocurrió un error al procesar el mensaje con Antigravity: $($_.Exception.Message)"
    }
    finally {
        $stopwatch.Stop()
    }
    $executionSeconds = [math]::Round($stopwatch.Elapsed.TotalSeconds, 2)

    if (-not $replyText -or $replyText.Trim() -eq "") {
        $replyText = "Sr Ramos, Antigravity completó la ejecución sin generar salida de texto directa."
    }

    $cleanReply = $replyText.Trim()
    $turnOutput = [math]::Ceiling($cleanReply.Length / 4)

    $timestamp = (Get-Date).ToString("HH:mm:ss")

    $userMsg = [PSCustomObject]@{
        id = [guid]::NewGuid().ToString()
        role = "user"
        content = $Message
        timestamp = $timestamp
        tokens = $turnInput
    }
    $assistantMsg = [PSCustomObject]@{
        id = [guid]::NewGuid().ToString()
        role = "assistant"
        content = $cleanReply
        timestamp = $timestamp
        tokens = $turnOutput
    }

    [void]$global:SessionTelemetry.Messages.Add($userMsg)
    [void]$global:SessionTelemetry.Messages.Add($assistantMsg)

    $global:SessionTelemetry.InputTokens += $effectiveInput
    $global:SessionTelemetry.OutputTokens += $turnOutput
    $global:SessionTelemetry.TotalTokens = $global:SessionTelemetry.InputTokens + $global:SessionTelemetry.OutputTokens

    $pct = [math]::Round(($global:SessionTelemetry.TotalTokens / $maxContext) * 100, 2)

    return [PSCustomObject]@{
        success = $true
        reply = $cleanReply
        timestamp = $timestamp
        executionSeconds = $executionSeconds
        tokens = [PSCustomObject]@{
            turnInput = $turnInput
            turnOutput = $turnOutput
            sessionTotal = $global:SessionTelemetry.TotalTokens
            sessionInput = $global:SessionTelemetry.InputTokens
            sessionOutput = $global:SessionTelemetry.OutputTokens
            model = $activeModel
            maxContext = $maxContext
            percent = $pct
        }
    }
}

function Read-RequestBody {
    param([System.Net.HttpListenerRequest]$Request)
    if (-not $Request.HasEntityBody) { return "" }
    $len = [int]$Request.ContentLength64
    if ($len -le 0) { return "" }
    $buffer = New-Object byte[] $len
    $read = 0
    while ($read -lt $len) {
        $r = $Request.InputStream.Read($buffer, $read, ($len - $read))
        if ($r -le 0) { break }
        $read += $r
    }
    return [System.Text.Encoding]::UTF8.GetString($buffer, 0, $read)
}

# Main Event Loop
while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $path = $request.Url.AbsolutePath
        $method = $request.HttpMethod
        
        if ($method -eq "OPTIONS") {
            Send-Response -Response $response -Content "" -StatusCode 200
            continue
        }
        
        # API Routes
        if ($path -eq "/api/status") {
            $statusObj = [PSCustomObject]@{
                status = "online"
                agent = "Beacon"
                user = "Sr Ramos"
                workspace = $workspaceRoot
                time = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                wtAvailable = (Test-Path "$env:LOCALAPPDATA\Microsoft\WindowsApps\wt.exe")
                activeModel = $global:SessionTelemetry.ActiveModel
                totalTokens = $global:SessionTelemetry.TotalTokens
                maxContext = Get-ModelMaxContext -model $global:SessionTelemetry.ActiveModel
            }
            Send-Response -Response $response -Content ($statusObj | ConvertTo-Json)
        }
        elseif ($path -eq "/api/skills") {
            $skillsData = Get-SkillsData
            Send-Response -Response $response -Content ($skillsData | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/subagents") {
            $subData = Get-SubagentsData
            Send-Response -Response $response -Content ($subData | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/graph") {
            $graphData = Get-GraphData
            Send-Response -Response $response -Content ($graphData | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/logs") {
            $logsData = Get-RecentLogs
            Send-Response -Response $response -Content ($logsData | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/performance") {
            $perfData = Get-PerformanceReport
            Send-Response -Response $response -Content ($perfData | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/chat/history") {
            $maxContext = Get-ModelMaxContext -model $global:SessionTelemetry.ActiveModel
            $pct = [math]::Round(($global:SessionTelemetry.TotalTokens / $maxContext) * 100, 2)
            $historyData = [PSCustomObject]@{
                messages = $global:SessionTelemetry.Messages
                tokens = [PSCustomObject]@{
                    sessionTotal = $global:SessionTelemetry.TotalTokens
                    sessionInput = $global:SessionTelemetry.InputTokens
                    sessionOutput = $global:SessionTelemetry.OutputTokens
                    model = $global:SessionTelemetry.ActiveModel
                    maxContext = $maxContext
                    percent = $pct
                }
            }
            Send-Response -Response $response -Content ($historyData | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/chat/clear" -and $method -eq "POST") {
            $global:SessionTelemetry.Messages.Clear()
            $global:SessionTelemetry.TotalTokens = 1500
            $global:SessionTelemetry.InputTokens = 1500
            $global:SessionTelemetry.OutputTokens = 0
            $maxContext = Get-ModelMaxContext -model $global:SessionTelemetry.ActiveModel
            $pct = [math]::Round((1500 / $maxContext) * 100, 2)
            
            $resObj = [PSCustomObject]@{
                success = $true
                tokens = [PSCustomObject]@{
                    sessionTotal = 1500
                    sessionInput = 1500
                    sessionOutput = 0
                    model = $global:SessionTelemetry.ActiveModel
                    maxContext = $maxContext
                    percent = $pct
                }
            }
            Send-Response -Response $response -Content ($resObj | ConvertTo-Json)
        }
        elseif ($path -eq "/api/model" -and $method -eq "POST") {
            $jsonBody = Read-RequestBody -Request $request
            $chosenModel = ""
            try {
                if ($jsonBody) {
                    $payloadObj = $jsonBody | ConvertFrom-Json
                    if ($payloadObj.model) { $chosenModel = $payloadObj.model.ToString().Trim() }
                }
            } catch {}
            
            if ($chosenModel) {
                $global:SessionTelemetry.ActiveModel = $chosenModel
            }
            $maxContext = Get-ModelMaxContext -model $global:SessionTelemetry.ActiveModel
            $pct = [math]::Round(($global:SessionTelemetry.TotalTokens / $maxContext) * 100, 2)
            
            $resObj = [PSCustomObject]@{
                success = $true
                model = $global:SessionTelemetry.ActiveModel
                maxContext = $maxContext
                totalTokens = $global:SessionTelemetry.TotalTokens
                percent = $pct
            }
            Send-Response -Response $response -Content ($resObj | ConvertTo-Json)
        }
        elseif ($path -eq "/api/chat" -and $method -eq "POST") {
            $jsonBody = Read-RequestBody -Request $request
            
            $msg = ""
            $mdl = ""
            try {
                if ($jsonBody) {
                    $payloadObj = $jsonBody | ConvertFrom-Json
                    if ($payloadObj.message) { $msg = $payloadObj.message.ToString() }
                    if ($payloadObj.model) { $mdl = $payloadObj.model.ToString() }
                }
            } catch {}
            
            if (-not $msg -or $msg.Trim() -eq "") {
                Send-Response -Response $response -Content '{"error": "Mensaje vacío"}' -StatusCode 400
                continue
            }
            
            $chatResult = Invoke-BeaconChat -Message $msg -Model $mdl
            Send-Response -Response $response -Content ($chatResult | ConvertTo-Json -Depth 5)
        }
        elseif ($path -eq "/api/launch" -and $method -eq "POST") {
            $jsonBody = Read-RequestBody -Request $request
            
            $payload = @{}
            try {
                if ($jsonBody) {
                    $payloadObj = $jsonBody | ConvertFrom-Json
                    foreach ($prop in $payloadObj.PSObject.Properties) {
                        $payload[$prop.Name] = $prop.Value
                    }
                }
            } catch {}

            $result = Launch-AntigravitySession -Data $payload
            Send-Response -Response $response -Content ($result | ConvertTo-Json)
        }
        # Static file routing
        else {
            $targetPath = ""
            if ($path -eq "/" -or $path -eq "/index.html") {
                $targetPath = Join-Path $publicDir "index.html"
            } else {
                $rel = $path.TrimStart('/') -replace '/', '\'
                $targetPath = Join-Path $publicDir $rel
            }
            Send-File -Response $response -FilePath $targetPath
        }
    }
    catch {
        Write-Warning "Error procesando petición: $_"
        try {
            if ($response) {
                Send-Response -Response $response -Content "{`"error`": `"Error interno: $($_.Exception.Message)`"}" -StatusCode 500
            }
        } catch {}
    }
}

