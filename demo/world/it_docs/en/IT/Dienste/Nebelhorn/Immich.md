---
Compose:
  - https://git.demo/studio/docker-compose-nebelhorn/src/branch/main/immich/compose.yaml
Gerät: "[[Nebelhorn]]"
URLs: [fotos.studio-weber.example.test]
Backup via: Borg
letzte Prüfung: {{day:-12}}
---
# Immich

Photos from the set and reference pictures.

```yaml
services:
  immich-server:
    image: ghcr.io/immich-app/immich-server:release
    volumes:
      - /srv/fotos:/usr/src/app/upload
```
