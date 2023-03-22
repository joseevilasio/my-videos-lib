import click
from flask import Flask

from api.controller import (
    add_new_video,
    delete_video,
    get_all_videos,
    get_video_by_id,
    update_video,
)


@click.group()
def controller():
    """Manage api"""


@controller.command("show")
def show():
    """List all videos"""
    for video in get_all_videos():
        click.echo(video)


@controller.command("show-by-id")
@click.argument("id")
def show_one():
    """List only one video by id"""
    click.echo(get_video_by_id())


def configure(app: Flask):
    app.cli.add_command(controller)
