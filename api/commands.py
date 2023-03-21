import click

from api.controller import (
    get_all_videos,
    get_video_by_id,
    add_new_video,
    update_video,
    delete_video,
)


@click.group()
def controller():
    """Manage api"""


def configure(app):
    app.cli.add_command(controller)
