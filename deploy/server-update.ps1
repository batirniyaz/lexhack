# Shared setup for running Docker over SSH on this machine (no access to the Windows credential manager there):
# a config copy without credential helpers + PATH without docker-credential-*.exe, docker.exe by full path.
$ProgressPreference = 'SilentlyContinue'
$dockerBin = 'C:\Users\batirniyaz\AppData\Local\Programs\DockerDesktop\resources\bin'
$env:DOCKER_CONFIG = 'D:\code\per\.docker-ssh'
$env:PATH = (($env:PATH -split ';') | Where-Object { $_ -and ($_ -notlike "$dockerBin*") }) -join ';'
$docker = Join-Path $dockerBin 'docker.exe'
Set-Location 'D:\code\per\lexhack'
& git fetch --quiet 'D:\code\per\probo.bundle' 'main:refs/remotes/bundle/main'
& git reset --hard bundle/main
cmd /c "`"$docker`" compose up -d --build > D:\code\per\probo-build.log 2>&1"
"exit code: $LASTEXITCODE"
Get-Content 'D:\code\per\probo-build.log' -Tail 12
"--- container:"
cmd /c "`"$docker`" ps --filter name=probo --format `"{{.Names}}  {{.Status}}  {{.Ports}}`" 2>&1"
Start-Sleep -Seconds 8
try { "health: " + (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8090/api/health -TimeoutSec 10).Content } catch { "health FAILED: $_" }
