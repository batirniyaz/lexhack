$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$cf = 'C:\Program Files (x86)\cloudflared\cloudflared.exe'
$cfg = "$env:USERPROFILE\.cloudflared\config.yml"
$tunnel = 'c7b534e0-51ee-4ab3-a8df-d3bd9eaa8da2'
$hostname = 'probo.aicenterkk.tech'

# 0. The app must answer locally before we route traffic to it.
try { "local health: " + (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8090/api/health -TimeoutSec 10).Content } catch { "local health FAILED: $_"; exit 1 }

# 1. Backup in the same style as the existing ones.
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
Copy-Item $cfg "$cfg.bak-$stamp"
"backup: $cfg.bak-$stamp"

# 2. Insert the ingress rule before the final catch-all, keeping encoding (BOM or not) and line endings.
$bytes = [IO.File]::ReadAllBytes($cfg)
$hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
$text = [Text.Encoding]::UTF8.GetString($bytes)
if ($hasBom) { $text = $text.Substring(1) }
if ($text.Contains($hostname)) {
  "rule already present"
} else {
  $nl = if ($text.Contains("`r`n")) { "`r`n" } else { "`n" }
  $marker = '  - service: http_status:404'
  $idx = $text.LastIndexOf($marker)
  if ($idx -lt 0) { "catch-all rule not found - aborting"; exit 1 }
  $rule = "  # Probo (LexHackathon): docker compose in D:\code\per\lexhack, container port 8000 -> 127.0.0.1:8090$nl" +
          "  - hostname: $hostname$nl" +
          "    service: http://localhost:8090$nl"
  $text = $text.Substring(0, $idx) + $rule + $text.Substring($idx)
  [IO.File]::WriteAllText($cfg, $text, (New-Object Text.UTF8Encoding($hasBom)))
  "rule inserted (bom=$hasBom)"
}

# 3. Validate before touching the running service.
& $cf tunnel --config $cfg ingress validate
if ($LASTEXITCODE -ne 0) { "VALIDATION FAILED - restoring backup"; Copy-Item "$cfg.bak-$stamp" $cfg -Force; exit 1 }
& $cf tunnel --config $cfg ingress rule "https://$hostname/"

# 4. DNS: CNAME probo -> the tunnel (no-op if it already exists).
& $cf tunnel route dns $tunnel $hostname

# 5. Restart the tunnel service to load the new rule.
Restart-Service Cloudflared
Start-Sleep -Seconds 6
"service: " + (Get-Service Cloudflared).Status
