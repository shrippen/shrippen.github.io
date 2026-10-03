---
tags:
  - IT
letzte Prüfung: {{day:-9}}
---
Entscheidungslog für die IT-Doku von Studio Weber. Bei Widerspruch zwischen einer Notiz und dieser Datei gilt diese Datei.

# Namen

Hosts heißen nach Seezeichen der Elbe:

| Name | Früher | Rolle |
| --- | --- | --- |
| [[Nebelhorn]] | SW-NAS01 | NAS im Studio |
| [[Feuerschiff]] | SW-VPS | gemieteter Server bei Nordhost |
| [[Boje]] | SW-PI | Raspberry Pi für DNS und Uptime |

Alte Codenamen nur noch in deprecated-Notizen.

# Dienstnotiz (Minimum)

Frontmatter: `Gerät`, `URLs`, `Backup via`, `letzte Prüfung`. Body: Zweck, Erreichbarkeit, Link zur `compose.yaml` in Gitea. Keine Compose-Vollkopien.

# Secrets

Keine Passwörter, Tokens oder Schlüssel im Klartext. Stattdessen `siehe Vaultwarden: {Eintrag}` oder `${ENV_NAME}`.

# Backup

Alle Hosts sichern mit Borg auf [[Nebelhorn]]. Restic ist abgelöst.
