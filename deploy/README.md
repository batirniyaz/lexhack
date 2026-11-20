# Deployment of the Probo demo

Public URL: **https://probo.aicenterkk.tech** (Cloudflare tunnel `stomadent` on Role 1's always-on Windows machine).

| What | Where |
|---|---|
| Code | `D:\code\per\lexhack` on the server (updated from a git bundle; the server has no GitHub access) |
| Secrets | `D:\code\per\lexhack\.env` on the server only |
| Container | `docker compose` service `probo`, `127.0.0.1:8090 -> 8000`, `restart: unless-stopped` |
| Data | `D:\code\per\lexhack\scans` (volume): scans, share links, LLM cache |
| Tunnel rule | `C:\Users\batirniyaz\.cloudflared\config.yml`: `probo.aicenterkk.tech -> http://localhost:8090` (backup `config.yml.bak-20261121-010441`) |

**Update the server after a push:** `bash deploy/push-to-server.sh` (bundle → scp → `server-update.ps1`: reset to the bundle,
`docker compose up -d --build`, health check).

**Docker over SSH:** `server-update.ps1` uses `D:\code\per\.docker-ssh` (a copy of `~/.docker` without a credential helper)
and removes Docker Desktop's `resources\bin` from `PATH`; otherwise every pull fails with "error getting credentials"
because an SSH session cannot reach the Windows credential manager.

`server-add-tunnel-route.ps1` is the one-time script that added the tunnel rule (backup → insert → validate → DNS → restart).
