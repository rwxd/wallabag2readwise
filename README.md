# wallabag2readwise

## Description

Pushes wallabag annotations from entries to Readwise highlights.

## Installation

```bash
python3 -m pip install wallabag2readwise
```

or with [pipx](https://github.com/pypa/pipx)

```bash
pipx install wallabag2readwise
```

## Usage

### Commands

```bash
wallabag2readwise push
```

### Configuration

Get a new Readwise API Token from [this url](https://readwise.io/access_token).

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
