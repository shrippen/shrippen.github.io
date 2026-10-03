---
Gerät: "[[Nebelhorn]]"
URLs: [fotos.studio-weber.example.test]
Backup via: Borg
letzte Prüfung: {{day:-12}}
---
# Immich

Fotos vom Set und Referenzbilder.

```yaml
services:
  immich-server:
    image: ghcr.io/immich-app/immich-server:release
    volumes:
      - /srv/fotos:/usr/src/app/upload
```
