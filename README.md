<br />
<p align="center">
  <!-- <a href="https://github.com/agentsea/skillpacks">
    <img src="https://project-logo.png" alt="Logo" width="80">
  </a> -->

  <h1 align="center">DeviceBay</h1>

  <p align="center">
    Devices for AI agents
    <br />
    <a href="https://github.com/agentsea/devicebay"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/agentsea/devicebay">View Demo</a>
    ·
    <a href="https://github.com/agentsea/devicebay/issues">Report Bug</a>
    ·
    <a href="https://github.com/agentsea/devicebay/issues">Request Feature</a>
  </p>
  <br>
</p>

DeviceBay offers pluggable devices ready to be used by AI agents, complete with a UI experience.

## Installation

```sh
pip install devicebay
```

## Supported Devices

- Desktops via [AgentDesk](https://github.com/agentsea/agentdesk)
- Filesystems via [FileSystem](./devicebay/devices/filesystem.py)
- Browsers via [Playwright](./devicebay/devices/browser.py)
- Repositories via [Github](./devicebay/devices/gh.py)

## Backends

Device configuration storage can be backed by:

- Sqlite
- Postgresql

Sqlite will be used by default. To use postgres simply configure the env vars:

```sh
DB_TYPE=postgres
DB_NAME=devices
DB_HOST=localhost
DB_USER=postgres
DB_PASS=abc123
```
