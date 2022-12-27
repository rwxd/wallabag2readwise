# wallabag2readwise

## Description

Exports / synchronizes annotations from [wallabag](https://github.com/wallabag/wallabag) to [Readwise](https://readwise.io/) article highlights.

This tool can be run as a cli tool or as a (docker) container.

Rate limiting of the Readwise API is supported.

## Installation

### CLI

```bash
pip install -U wallabag2readwise
```

or with [pipx](https://github.com/pypa/pipx)

```bash
pipx install wallabag2readwise
```

### Docker / Container

```bash
docker pull ghcr.io/rwxd/wallabag2readwise:latest
```

```bash
docker run ghcr.io/rwxd/wallabag2readwise:latest --wait-time 60 ...
```

#### Docker-Compose

```yaml
version: "3.9"
services:
  wallabag2readwise:
    image: ghcr.io/rwxd/wallabag2readwise:latest
    container_name: wallabag2readwise
    restart: unless-stopped
    environment:
      READWISE_TOKEN: ''
      WALLABAG_URL: ''
      WALLABAG_USER: ''
      WALLABAG_PASSWORD: ''
      WALLABAG_CLIENT_ID: ''
      WALLABAG_CLIENT_SECRET: ''
    # env_file:
    #  - .env
```

```bash
docker-compose up -d && docker-compose logs -f
```

## Usage

### Commands

```bash
wallabag2readwise push
```

#### Daemon

Run continuously and push new annotations to Readwise every 60 minutes.
(The container is automatically in daemon mode.)

```bash
wallabag2readwise daemon --wait-time 60
```

### Configuration

Get a new Readwise API Token from <https://readwise.io/access_token>.

Create a new wallabag API client in your instance <https://my-wallabag.com/developer/client/create>.

#### ENV Vars

```bash
READWISE_TOKEN=''
WALLABAG_URL=''
WALLABAG_USER=''
WALLABAG_PASSWORD=''
WALLABAG_CLIENT_ID=''
WALLABAG_CLIENT_SECRET=''
```

#### CLI Options

Secrets can also be used with cli options.

All cli options can be viewed with `wallabag2readwise --help`
