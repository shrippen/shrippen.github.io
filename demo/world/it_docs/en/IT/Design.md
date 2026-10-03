---
tags:
  - IT
letzte Prüfung: {{day:-9}}
---
Decision log for Studio Weber's IT documentation. If a note contradicts this file, this file wins.

# Names

Hosts are named after Elbe sea marks:

| Name | Former | Role |
| --- | --- | --- |
| [[Nebelhorn]] | SW-NAS01 | NAS in the studio |
| [[Feuerschiff]] | SW-VPS | rented server at Nordhost |
| [[Boje]] | SW-PI | Raspberry Pi for DNS and uptime |

Old code names only in deprecated notes.

# Service note (minimum)

Frontmatter: `Gerät`, `URLs`, `Backup via`, `letzte Prüfung`. Body: purpose, reachability, link to the `compose.yaml` in Gitea. No full compose copies.

# Secrets

No passwords, tokens or keys in plain text. Use `siehe Vaultwarden: {entry}` or `${ENV_NAME}` instead.

# Backup

All hosts back up with Borg to [[Nebelhorn]]. Restic is retired.
