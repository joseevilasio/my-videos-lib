import json

import click
from flask import Flask

from api.controller import (
    add_new_category,
    add_new_video,
    delete_category,
    delete_video,
    get_all_category,
    get_all_videos,
    get_category_by_id,
    get_video_by_id,
    search_video,
    update_category,
    update_video,
    get_all_videos_by_category
)


@click.group()
def controller():
    """Manage >> MyVideosLIB API <<"""


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


@controller.command("search")
@click.argument("search_word", type=click.STRING, required=True)
def search(search_word):
    """List all videos match with search"""
    result = search_video(search_word)
    click.echo(result)


# COMMANDS CATEGORY


@controller.command("show-category")
def show_category():
    """List all category"""
    result = get_all_category()
    click.echo(result)


@controller.command("show-category-by-id")
@click.argument("id", type=click.STRING, required=True)
def show_one_category(id):
    """List only one category by id"""
    click.echo(get_category_by_id(int(id)))


@controller.command("new-category")
@click.argument("data", required=True)
def new_category(data):
    """Add new category on database"""

    with open(data, "r") as data_json:
        data_dict = json.load(data_json)

    result = add_new_category(data_dict)
    click.echo(get_category_by_id(result))


@controller.command("delete-category")
@click.argument("id", type=click.STRING, required=True)
def delete_category(id):
    """Delete one category by id"""
    result = delete_category(int(id))
    click.echo(result)


@controller.command("update-category")
@click.argument("id", type=click.INT, required=True)
@click.argument("data", required=False)
def update_category(id, data):
    """Update category infor on database"""
    with open(data, "r") as data_json:
        data_dict = json.load(data_json)

    result = update_category(int(id), data_dict)
    click.echo(get_category_by_id(result))


# COMMANDS RELATIONSHIP


@controller.command("show-videos-by-category")
@click.argument("id", type=click.STRING, required=True)
def show_videos_by_category(id):
    """List all videos by category"""
    result = get_all_videos_by_category(int(id))
    click.echo(result)


def configure(app: Flask):
    app.cli.add_command(controller)
