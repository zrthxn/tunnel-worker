# Tunnel Worker
A Docker container that monitors SSH tunnels and revives those which are broken.

## Useage
You can use this two ways.

### Single tunnel
```yaml
# Single tunnel
services:
  tunnler:
    image: this
    container_name: tunnel-worker
    restart: unless-stopped
    environment:
      - PING_INTERVAL=3600
      - REMOTE_HOST=host
      - ACCESS_PORT=22
      - SSHKEY_FILE=/keys/host
      - TUNNEL_PORT=8000

      - TARGET_HOST=localhost
      - TARGET_PORT=80
      - REMOTE_PING_PORT=80
      - REMOTE_PING_VERB=GET
      - FAIL_STATUS=502
    volumes:
      - ./tunnel:/config
      - ./keys:/keys
```

### Multi tunnel
```yaml
# Multi tunnel
services:
  tunnler:
    image: this
    container_name: tunnel-worker
    restart: unless-stopped
    environment:
      - PING_INTERVAL=3600
      - CONFIG_FILE=/config/config.yaml
    volumes:
      - ./tunnel:/config
      - ./keys:/keys
```
```yaml
# Config.yaml
satellites:
  one:
    REMOTE_HOST: "host"
    ACCESS_PORT: 22
    SSHKEY_FILE: "/keys/host"
    TUNNEL_PORT: 8000

    TARGET_HOST: "localhost"
    TARGET_PORT: 80
    REMOTE_PING_PORT: 80
    REMOTE_PING_VERB: "GET"
    FAIL_STATUS: 502
```
