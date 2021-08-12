# Tunnel Worker
A Docker container that monitors SSH tunnels and revives those which are broken.

Numerous autossh containers didn't work for me. Other means of establishing a TCP tunnel
also failed. So I had to write this. It works.
This container will start and maintain SSH tunnels by periodically checking the remote 
hosts (satellites) and if the response is incorrect, it will kill and start a new `ssh` process.


## Usage
You can use this two ways, depending on whether you want to maintain a single tunnel
or multiple tunnels, you either use the `environment` variables or you use the config file respectively.

The meaning and useage of each variable is given [here](#Variables).

### Single tunnel
Using the `environment` variables we can create and maintain a single tunnel.
```yaml
# Single tunnel
services:
  tunnler:
    image: zrthxn/tunnel:latest
    container_name: tunnel-worker
    restart: unless-stopped
    environment:
      - PING_INTERVAL=3600
      - REMOTE_HOST=host
      - ACCESS_PORT=22
      - SSHKEY_FILE=/keys/host
      - TUNNEL_PORT=8000

      - TUNNEL_MODE=-R
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
Using the config file we can create and maintain a many tunnels.
```yaml
# Multi tunnel
services:
  tunnler:
    image: zrthxn/tunnel:latest
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

    TUNNEL_MODE: "-R"
    TARGET_HOST: "localhost"
    TARGET_PORT: 80
```

### Variables

| Variable Name    | Where         | Default     | Description                                                  |
| ---------------- | ------------- | ----------- | ------------------------------------------------------------ |
| PING_INTERVAL    | environment   | -           | The interval of time after which each remote host is checked. |
| CONFIG_FILE      | environment   | -           | Path to `config.yml` file.                                   |
| REMOTE_HOST      | config or env | -           | The hostname or IP of the remote host.                       |
| ACCESS_PORT      | config or env | 22          | The port of the remote host to SSH into.                     |
| SSHKEY_FILE      | config or env | -           | The SSH identity key file.                                   |
| TUNNEL_PORT      | config or env | -           | The port on the remote to open for tunnel.                   |
| TUNNEL_MODE      | config or env | `-R`        | "-R" means local to remote, "-L" means remote to local.      |
| TARGET_HOST      | config or env | `localhost` | The other end of the tunnel.                                 |
| TARGET_PORT      | config or env | 80          | The port on the other end.                                   |
| REMOTE_PING_PORT | config or env | 80          | The port of the remote to check.                             |
| REMOTE_PING_VERB | config or env | **GET**     | The HTTP request verb to use while checking.                 |
| FAIL_STATUS      | config or env | 502         |                                                              |