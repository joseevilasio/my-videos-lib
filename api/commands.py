import json

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
    """Manage MyVideosLIB API"""


@controller.command("show")
def show():
    """List all videos"""
    result = get_all_videos()
    click.echo(result)


@controller.command("show-by-id")
@click.argument("id", type=click.STRING, required=True)
def show_one(id):
    """List only one video by id"""
    click.echo(get_video_by_id(int(id)))


@controller.command("new-video")
@click.argument("data", required=True)
def new_video(data):
    """Add new video on database"""

    with open(data, "r") as data_json:
        data_dict = json.load(data_json)

    result = add_new_video(data_dict)
    click.echo(get_video_by_id(result))


@controller.command("delete")
@click.argument("id", type=click.STRING, required=True)
def delete(id):
    """Delete one video by id"""
    result = delete_video(int(id))
    click.echo(result)


@controller.command("update-video")
@click.argument("id", type=click.INT, required=True)
@click.argument("data", required=False)
def update(id, data):
    """Update video infor on database"""
    with open(data, "r") as data_json:
        data_dict = json.load(data_json)

    result = update_video(int(id), data_dict)
    click.echo(get_video_by_id(result))


def configure(app: Flask):
    app.cli.add_command(controller)
