from flask import Blueprint, Flask, redirect, url_for

from api.controller import (
    add_new_video,
    delete_video,
    get_all_videos,
    get_video_by_id,
    update_video,
)

bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return "api - lib videos"


@bp.route("/videos")
def list_videos():
    videos = get_all_videos()
    return videos


@bp.route("/videos/<int:video_id>")
def one_video(video_id):
    video = get_video_by_id(video_id)
    return video


@bp.route("/videos/<int:video_id>")
def delete_one_video(video_id):
    video = delete_video(video_id)
    return video


@bp.route("/videos/new", methods=["GET", "POST"])
def new_video(title, description, url):
    # TODO: Feature futura
    video = add_new_video(title, description, url)
    return video


@bp.route("/videos/<int:video_id>", methods=["GET", "POST"])
def update_data_video(video_id, title, description, url):
    # TODO: Atualizar com construção de dados
    video = update_video(video_id, title, description, url)
    updated = redirect(url_for("api.one_video", video_id=video_id))
    return video, updated


def configure(app: Flask):
    app.register_blueprint(bp)
