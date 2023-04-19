from flask import Blueprint, Flask, abort, request

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
    return "Hello, World! MyVideos API", 200


@bp.route("/videos")
def list_videos():
    videos = get_all_videos()
    if not videos:
        return abort(404)
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


@bp.route("/videos/new", methods=["POST", "GET"])
def new_video():
    data = request.get_json()
    video = add_new_video(data)
    return video


@bp.route("/videos/<int:video_id>", methods=["PUT", "GET"])
def update_data_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return video


@bp.route("/videos/<int:video_id>", methods=["PATCH", "GET"])
def update_partial_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return video


def configure(app: Flask):
    app.register_blueprint(bp)
