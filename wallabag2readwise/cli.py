import typer
from wallabag2readwise.misc import push_annotations
from wallabag2readwise.readwise import ReadwiseConnector

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
    readwise = ReadwiseConnector(readwise_token)
    push_annotations(wallabag, readwise)


# TODO: Daemon
# @app.command()
# def daemon():
#     pass
