import importlib.metadata
from time import sleep

import typer
from readwise import Readwise, ReadwiseReader

from wallabag2readwise.misc import push_annotations
from wallabag2readwise.output import console
from wallabag2readwise.wallabag import WallabagConnector

app = typer.Typer()


@app.command()
def push(
    wallabag_url: str = typer.Option(
        ..., envvar='WALLABAG_URL', help='url to your wallabag instance'
    ),
    wallabag_user: str = typer.Option(..., envvar='WALLABAG_USER'),
    wallabag_password: str = typer.Option(..., envvar='WALLABAG_PASSWORD', prompt=True),
    wallabag_client_id: str = typer.Option(..., envvar='WALLABAG_CLIENT_ID'),
    wallabag_client_secret: str = typer.Option(..., envvar='WALLABAG_CLIENT_SECRET'),
    readwise_token: str = typer.Option(..., envvar='READWISE_TOKEN', prompt=True),
):
    wallabag = WallabagConnector(
        wallabag_url,
        wallabag_user,
        wallabag_password,
        wallabag_client_id,
        wallabag_client_secret,
    )
    readwise = Readwise(readwise_token)
    push_annotations(wallabag, readwise)


@app.command()
def daemon(
    wallabag_url: str = typer.Option(
        ..., envvar='WALLABAG_URL', help='url to your wallabag instance'
    ),
    wallabag_user: str = typer.Option(..., envvar='WALLABAG_USER'),
    wallabag_password: str = typer.Option(..., envvar='WALLABAG_PASSWORD', prompt=True),
    wallabag_client_id: str = typer.Option(..., envvar='WALLABAG_CLIENT_ID'),
    wallabag_client_secret: str = typer.Option(..., envvar='WALLABAG_CLIENT_SECRET'),
    readwise_token: str = typer.Option(..., envvar='READWISE_TOKEN', prompt=True),
    wait_time: int = typer.Option(
        60, help='time to wait between runs in minutes', envvar='WAIT_TIME'
    ),
) -> None:
    console.print(f'> Starting daemon with {wait_time} minutes wait time')
    while True:
        wallabag = WallabagConnector(
            wallabag_url,
            wallabag_user,
            wallabag_password,
            wallabag_client_id,
            wallabag_client_secret,
        )
        readwise = Readwise(readwise_token)
        push_annotations(wallabag, readwise)

        console.print(f'=> Waiting {wait_time} minutes')
        sleep(wait_time * 60)


@app.command()
def reader(
    wallabag_url: str = typer.Option(
        ..., envvar='WALLABAG_URL', help='url to your wallabag instance'
    ),
    wallabag_user: str = typer.Option(..., envvar='WALLABAG_USER'),
    wallabag_password: str = typer.Option(..., envvar='WALLABAG_PASSWORD', prompt=True),
    wallabag_client_id: str = typer.Option(..., envvar='WALLABAG_CLIENT_ID'),
    wallabag_client_secret: str = typer.Option(..., envvar='WALLABAG_CLIENT_SECRET'),
    readwise_token: str = typer.Option(..., envvar='READWISE_TOKEN', prompt=True),
):
    console.print('> Starting readwise reader import')
    wallabag = WallabagConnector(
        wallabag_url,
        wallabag_user,
        wallabag_password,
        wallabag_client_id,
        wallabag_client_secret,
    )
    readwise = ReadwiseReader(readwise_token)
    wallabag_entries = wallabag.get_entries()
    for entry in wallabag_entries:
        console.print(f'=> Importing {entry.title}')
        location = 'archive' if entry.archived else 'new'
        try:
            readwise.create_document(
                entry.url, tags=[t.label for t in entry.tags], location=location
            )
        except Exception as e:
            console.print(f'==> Error: {e}')


@app.command()
def version():
    console.print(importlib.metadata.version('wallabag2readwise'))
