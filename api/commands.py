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
    result = get_all_videos()
    click.echo(result)


@controller.command("show-by-id")
@click.argument("id")
def show_one(id):
    """List only one video by id"""
    result = get_video_by_id(id)
    click.echo(result)


@controller.command("new-video")
@click.argument("title", type=click.STRING, required=True)
@click.argument("description", type=click.STRING, required=True)
@click.argument("url", type=click.STRING, required=True)
def new_video(title, description, url):
    """Add new video on database"""
    result = add_new_video(title, description, url)
    print(result)


def configure(app: Flask):
    app.cli.add_command(controller)
