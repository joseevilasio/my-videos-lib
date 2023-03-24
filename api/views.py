from flask import Blueprint, Flask, abort, redirect, url_for

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
    return ""


@bp.route("/videos")
def list_videos():
    videos = get_all_videos()
    return videos


@bp.route("/videos/<int:video_id>")
def one_video(video_id):
    video = get_video_by_id(video_id)
    if not video:
        return abort(404)
    return video


@bp.route("/videos/<int:video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = get_video_by_id(video_id)
    if not video:
        return abort(404)
    else:
        exec_video = delete_video(video_id)
        return exec_video


@bp.route("/videos/new", methods=["GET", "POST"])
def new_video(**data):
    # TODO: Feature futura
    video = add_new_video(**data)
    return video


@bp.route("/videos/<int:video_id>", methods=["PUT"])
def update_data_video(video_id, **data):
    # TODO: Atualizar com construção de dados
    video = update_video(video_id, **data)
    updated = redirect(url_for("api.one_video", video_id=video_id))
    return video, updated


def configure(app: Flask):
    app.register_blueprint(bp)
