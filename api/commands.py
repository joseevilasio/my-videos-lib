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
def show_one(id, type=click.STRING, required=True):
    """List only one video by id"""
    result = get_video_by_id(id)
    click.echo(result or "not found")


@controller.command("new-video")
@click.argument("title", type=click.STRING, required=True)
@click.argument("description", type=click.STRING, required=True)
@click.argument("url", type=click.STRING, required=True)
def new_video(title, description, url):
    """Add new video on database"""
    result = add_new_video(title, description, url)
    # TODO: Adicionar retorno com os dados do video adicionado
    print(result)


@controller.command("delete")
@click.argument("id", type=click.STRING, required=True)
def delete(id):
    """Delete one video by id or all videos on database"""
    result = delete_video(id)
    print(result)


@controller.command("update-video")
@click.argument("id", type=click.STRING, required=True)
@click.argument("title", type=click.STRING, required=False)
@click.argument("description", type=click.STRING, required=False)
@click.argument("url", type=click.STRING, required=False)
def update(id, title=None, description=None, url=None):
    """Update video infor on database"""
    result = update_video(id, title, description, url)
    result_get = get_video_by_id(id)
    print(result)
    click.echo(result_get)


def configure(app: Flask):
    app.cli.add_command(controller)
