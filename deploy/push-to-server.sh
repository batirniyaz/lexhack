#!/usr/bin/env bash
# Update the Probo demo on the always-on Windows machine "batya" (SSH alias) from this repo.
# The server has no GitHub access, so the code travels as a git bundle; .env stays on the server.
#   bash deploy/push-to-server.sh
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
git bundle create "$TMP/probo.bundle" --all
scp -o BatchMode=yes "$TMP/probo.bundle" batya:D:/code/per/
ENC=$(iconv -f utf-8 -t utf-16le deploy/server-update.ps1 | base64 -w0)
ssh -o BatchMode=yes batya "powershell -NoProfile -NonInteractive -EncodedCommand $ENC" 2>&1 | grep -v -E "CLIXML|<Objs|post-quantum|store now|upgraded"
rm -rf "$TMP"
