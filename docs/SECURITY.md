# Security & secrets policy

## Never commit secrets
The GitHub token and the NVIDIA/Nemotron API key live **outside** this repository
(in the parent planning folder) and are matched by `.gitignore` patterns
(`*token*.txt`, `*API_key*.txt`, `**/nvidia_api_key*`, `.env`, …). If you ever add
a credential file, confirm `git status` does not list it before committing.

## Credentials at runtime
All credentials are read from environment variables:

| Variable | Use |
|---|---|
| `NVIDIA_API_KEY` | cloud Nemotron (NVIDIA NIM) |
| `VM_HOST`, `VM_USER`, `VM_PORT` | VM SSH target |
| `VM_KEY` *or* `VM_PASSWORD` | VM auth (key preferred) |
| `GITHUB_TOKEN` | release automation only |

## VM access
The plan recommends **key-based SSH**: generate a keypair, add the public key to
the VM `~/.ssh/authorized_keys`, and connect via the SSH agent. Password auth is
supported by `deploy/remote.py` (`VM_PASSWORD`) for convenience but should be
rotated and replaced with a key. The VM has a private IP (10.30.x.x); reach hosted
services through an SSH tunnel or the authenticated Caddy proxy.

## Patient data
This remains decision support. **No real patient data** is stored in the repo or
in any public/hosted artifact (gate G5). The public demo runs on synthetic +
public data only. No PHI is written to logs or the audit ledger in hosted contexts.
