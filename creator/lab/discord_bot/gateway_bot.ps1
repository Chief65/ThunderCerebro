param(
    [string]$TargetMessageId = ""
)

$envFile = Join-Path $PSScriptRoot ".env"
$envLines = Get-Content $envFile
$token = ($envLines | Where-Object { $_ -match "^DISCORD_BOT_TOKEN=(.+)" } | ForEach-Object { $matches[1] }).Trim()
$channelId = ($envLines | Where-Object { $_ -match "^DISCORD_CHANNEL_ID=(.+)" } | ForEach-Object { $matches[1] }).Trim()

$dbFile = Join-Path $PSScriptRoot "sorteos_db.json"
if (-not (Test-Path $dbFile)) {
    [System.IO.File]::WriteAllText($dbFile, '{"entries":[]}', [System.Text.Encoding]::UTF8)
}

$cfgFile = Join-Path $PSScriptRoot "sorteo_config.json"
$cfgJson = [System.IO.File]::ReadAllText($cfgFile, [System.Text.Encoding]::UTF8)
$cfg = $cfgJson | ConvertFrom-Json

function Get-Entries {
    $raw = [System.IO.File]::ReadAllText($dbFile, [System.Text.Encoding]::UTF8)
    $obj = $raw | ConvertFrom-Json
    if (-not $obj.entries) { return @() }
    return @($obj.entries)
}

function Save-Entries($entries) {
    $json = @{ entries = @($entries) } | ConvertTo-Json -Depth 5
    [System.IO.File]::WriteAllText($dbFile, $json, [System.Text.Encoding]::UTF8)
}

function Send-InteractionResponse($id, $interactionToken, $bodyObj) {
    $url = "https://discord.com/api/v10/interactions/$id/$interactionToken/callback"
    $json = $bodyObj | ConvertTo-Json -Depth 10
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $headers = @{
        "User-Agent" = "DiscordBot (https://thundermc.es, 1.0.0)"
    }
    try {
        Invoke-RestMethod -Uri $url -Method Post -Headers $headers -ContentType "application/json; charset=utf-8" -Body $bytes | Out-Null
        Write-Host ("Callback enviado exitosamente a interaccion " + $id) -ForegroundColor Cyan
    } catch {
        Write-Warning ("Fallo callback: " + $_)
    }
}

function Update-GiveawayMessage($targetMsgId, $newCount) {
    $msgUrl = "https://discord.com/api/v10/channels/$channelId/messages/$targetMsgId"
    $headers = @{
        "Authorization" = "Bot $token"
        "User-Agent" = "DiscordBot (https://thundermc.es, 1.0.0)"
    }

    try {
        $currentMsg = Invoke-RestMethod -Uri $msgUrl -Method Get -Headers $headers
        if ($currentMsg.embeds -and $currentMsg.embeds.Count -gt 0) {
            $embed = $currentMsg.embeds[0]
            
            $findPattern = 'Entradas registradas: `\d+ participantes`'
            $replaceText = 'Entradas registradas: `' + $newCount + ' participantes`'
            $embed.description = [regex]::Replace($embed.description, $findPattern, $replaceText)
            
            $patchBody = @{
                embeds = @($embed)
            } | ConvertTo-Json -Depth 10
            $patchBytes = [System.Text.Encoding]::UTF8.GetBytes($patchBody)
            
            Invoke-RestMethod -Uri $msgUrl -Method Patch -Headers $headers -ContentType "application/json; charset=utf-8" -Body $patchBytes | Out-Null
            Write-Host ("Live update Discord mensaje " + $targetMsgId + ": " + $newCount + " participantes") -ForegroundColor Green
        }
    } catch {
        Write-Warning ("Error al actualizar mensaje: " + $_)
    }
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  THUNDERMC - GATEWAY BOT EN TIEMPO REAL (SORTEOS)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ("Canal: " + $channelId)

while ($true) {
    $ws = $null
    $cts = $null
    try {
        $ws = New-Object System.Net.WebSockets.ClientWebSocket
        $cts = New-Object System.Threading.CancellationTokenSource
        $uri = [Uri]("wss://gateway.discord.gg/?v=10" + [char]38 + "encoding=json")

        Write-Host "Conectando al Gateway de Discord..." -ForegroundColor Yellow
        $ws.ConnectAsync($uri, $cts.Token).Wait()

        if ($ws.State -ne [System.Net.WebSockets.WebSocketState]::Open) {
            Write-Warning "Fallo al abrir WebSocket. Reintentando..."
            Start-Sleep -Seconds 5
            continue
        }

        Write-Host "Conectado al Gateway de Discord exitosamente." -ForegroundColor Green

        $buffer = New-Object Byte[] 32768
        $heartbeatTimer = $null
        $seq = $null
        $interval = 41250
        $nextHeartbeat = 41250

        while ($ws.State -eq [System.Net.WebSockets.WebSocketState]::Open) {
            if ($heartbeatTimer -and ($heartbeatTimer.ElapsedMilliseconds -ge $nextHeartbeat)) {
                $hbJson = @{ op = 1; d = $seq } | ConvertTo-Json -Depth 5 -Compress
                $hbBytes = [System.Text.Encoding]::UTF8.GetBytes($hbJson)
                $hbSeg = New-Object System.ArraySegment[Byte] -ArgumentList @(,$hbBytes)
                $ws.SendAsync($hbSeg, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()
                $nextHeartbeat = $heartbeatTimer.ElapsedMilliseconds + $interval
                Write-Host "Heartbeat enviado (keep-alive OK)" -ForegroundColor DarkGray
            }

            $ms = New-Object System.IO.MemoryStream
            $closed = $false
            do {
                $segment = New-Object System.ArraySegment[Byte] -ArgumentList @(,$buffer)
                $recvTask = $ws.ReceiveAsync($segment, $cts.Token)

                while (-not $recvTask.Wait(500)) {
                    if ($ws.State -ne [System.Net.WebSockets.WebSocketState]::Open) {
                        $closed = $true
                        break
                    }
                    if ($heartbeatTimer -and ($heartbeatTimer.ElapsedMilliseconds -ge $nextHeartbeat)) {
                        $hbJson = @{ op = 1; d = $seq } | ConvertTo-Json -Depth 5 -Compress
                        $hbBytes = [System.Text.Encoding]::UTF8.GetBytes($hbJson)
                        $hbSeg = New-Object System.ArraySegment[Byte] -ArgumentList @(,$hbBytes)
                        $ws.SendAsync($hbSeg, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()
                        $nextHeartbeat = $heartbeatTimer.ElapsedMilliseconds + $interval
                        Write-Host "Heartbeat enviado (keep-alive OK)" -ForegroundColor DarkGray
                    }
                }

                if ($closed -or ($ws.State -ne [System.Net.WebSockets.WebSocketState]::Open)) {
                    $closed = $true
                    break
                }

                $res = $recvTask.Result
                if ($res.MessageType -eq [System.Net.WebSockets.WebSocketMessageType]::Close) {
                    Write-Warning "Gateway cerrado por Discord."
                    $closed = $true
                    break
                }
                $ms.Write($buffer, 0, $res.Count)
            } while (-not $res.EndOfMessage)

            if ($closed) { break }
            if ($ms.Length -eq 0) { continue }

            $payloadStr = [System.Text.Encoding]::UTF8.GetString($ms.ToArray())
            $payload = $payloadStr | ConvertFrom-Json

            if ($payload.s) { $seq = $payload.s }

            if ($payload.op -eq 10) {
                $interval = $payload.d.heartbeat_interval
                Write-Host ("Recibido Hello. Heartbeat: " + $interval + " ms") -ForegroundColor Cyan
                
                $idJson = @{
                    op = 2
                    d = @{
                        token = $token
                        intents = 0
                        properties = @{
                            os = "windows"
                            browser = "thundermc_bot"
                            device = "thundermc_bot"
                        }
                    }
                } | ConvertTo-Json -Depth 5 -Compress
                $idBytes = [System.Text.Encoding]::UTF8.GetBytes($idJson)
                $idSeg = New-Object System.ArraySegment[Byte] -ArgumentList @(,$idBytes)
                $ws.SendAsync($idSeg, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()
                Write-Host "Identificacion enviada al Gateway." -ForegroundColor Green

                $heartbeatTimer = [System.Diagnostics.Stopwatch]::StartNew()
                $nextHeartbeat = $interval
            }

            if ($payload.op -eq 11) {
                Write-Host "Heartbeat ACK recibido." -ForegroundColor DarkGray
            }

            if ($payload.op -eq 0) {
                if ($payload.t -eq "READY") {
                    Write-Host ("Bot activo: " + $payload.d.user.username) -ForegroundColor Green
                    Write-Host "Esperando clicks en Discord en tiempo real..." -ForegroundColor Yellow
                }

                if ($payload.t -eq "INTERACTION_CREATE") {
                    $interaction = $payload.d
                    $customId = $interaction.data.custom_id
                    $userId = $interaction.user.id
                    $userName = $interaction.user.username
                    if ($interaction.member) {
                        $userId = $interaction.member.user.id
                        $userName = $interaction.member.user.username
                    }
                    $interId = $interaction.id
                    $interToken = $interaction.token
                    $interMsgId = $interaction.message.id

                    Write-Host ("INTERACCION: [" + $userName + "] (" + $userId + ") -> " + $customId) -ForegroundColor Magenta

                    if ($customId -eq "sorteo_participar") {
                        $entries = Get-Entries
                        $already = $entries | Where-Object { $_.userId -eq $userId }

                        if ($already) {
                            Write-Host ("Usuario " + $userName + " ya registrado.") -ForegroundColor Yellow
                            $resp = @{
                                type = 4
                                data = @{
                                    flags = 64
                                    content = $cfg.already_registered
                                }
                            }
                            Send-InteractionResponse $interId $interToken $resp
                        } else {
                            $newEntry = @{
                                userId = $userId
                                username = $userName
                                joinedAt = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
                            }
                            $entries = @($entries) + @($newEntry)
                            Save-Entries $entries
                            
                            Write-Host ("NUEVA ENTRADA: " + $userName + " | Total: " + $entries.Count) -ForegroundColor Green

                            $resp = @{
                                type = 4
                                data = @{
                                    flags = 64
                                    content = $cfg.success_registration
                                }
                            }
                            Send-InteractionResponse $interId $interToken $resp

                            Update-GiveawayMessage $interMsgId $entries.Count
                        }
                    } elseif ($customId -eq "sorteo_ver_estado") {
                        $entries = Get-Entries
                        $userEntry = $entries | Where-Object { $_.userId -eq $userId }

                        $content = $cfg.status_not_registered
                        if ($userEntry) {
                            $content = $cfg.status_registered + " (Registrado: <t:" + $userEntry.joinedAt + ":R>)"
                        }

                        $resp = @{
                            type = 4
                            data = @{
                                flags = 64
                                content = $content
                            }
                        }
                        Send-InteractionResponse $interId $interToken $resp
                    }
                }
            }
        }
    } catch {
        Write-Warning ("Excepcion en Gateway: " + $_)
    } finally {
        if ($ws -and ($ws.State -eq [System.Net.WebSockets.WebSocketState]::Open)) {
            try { $ws.CloseAsync([System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure, "Cerrando", [System.Threading.CancellationToken]::None).Wait(1000) } catch {}
        }
    }
    Write-Host "Reconectando en 5 segundos..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}
