from flask import Blueprint, Flask, abort, jsonify, redirect, request, url_for

from api.controller import (
    add_new_category,
    add_new_video,
    delete_category,
    delete_video,
    get_all_category,
    get_all_videos,
    get_all_videos_by_category,
    get_category_by_id,
    get_video_by_id,
    search_video,
    update_category,
    update_video,
)

bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return "Hello, World! MyVideosLIB API", 200


@bp.route("/videos")
def list_videos():
    videos = get_all_videos()
    if not videos:
        return abort(404)
    return jsonify(videos), 200


@bp.route("/videos/<int:video_id>")
def one_video(video_id):
    video = get_video_by_id(video_id)
    if not video:
        return abort(404)
    return jsonify(video), 200


@bp.route("/videos/<int:video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = get_video_by_id(video_id)
    if not video:
        return abort(404)
    else:
        exec_video = delete_video(video_id)
        return exec_video


@bp.route("/videos/new", methods=["GET", "POST"])
def new_video():
    data = request.get_json()
    video = add_new_video(data)
    return redirect(url_for("api.one_video", video_id=video))


@bp.route("/videos/<int:video_id>", methods=["GET", "PUT"])
def update_data_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return redirect(url_for("api.one_video", video_id=video))


@bp.route("/videos/<int:video_id>", methods=["GET", "PATCH"])
def update_partial_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return redirect(url_for("api.one_video", video_id=video))


@bp.route("/videos/")
def search_video_query():
    search = request.args.get("search")
    videos = search_video(search)
    if not videos:
        return abort(404)
    return jsonify(videos), 200


# CATEGORY ROUTES


@bp.route("/category")
def list_category():
    category = get_all_category()
    if not category:
        return abort(404)
    return jsonify(category), 200


@bp.route("/category/<int:categoryId>")
def one_category(categoryId):
    category = get_category_by_id(categoryId)
    if not category:
        return abort(404)
    return jsonify(category), 200


@bp.route("/category/<int:categoryId>", methods=["DELETE"])
def delete_one_category(categoryId):
    category = get_category_by_id(categoryId)
    if not category:
        return abort(404)
    else:
        exec_category = delete_category(categoryId)
        return exec_category


@bp.route("/category/new", methods=["GET", "POST"])
def new_category():
    data = request.get_json()
    category = add_new_category(data)
    return redirect(url_for("api.one_category", categoryId=category))


@bp.route("/category/<int:categoryId>", methods=["GET", "PUT"])
def update_data_category(categoryId):
    data = request.get_json()
    category = update_category(categoryId, data)
    return redirect(url_for("api.one_category", categoryId=category))


@bp.route("/category/<int:categoryId>", methods=["GET", "PATCH"])
def update_partial_category(categoryId):
    data = request.get_json()
    category = update_category(categoryId, data)
    return redirect(url_for("api.one_category", categoryId=category))


# RELATIONSHIP


@bp.route("/category/<int:categoryId>/videos", methods=["GET"])
def show_videos_by_category(categoryId):
    videos_category = get_all_videos_by_category(categoryId)
    if not videos_category:
        return abort(404)
    return jsonify(videos_category), 200


def configure(app: Flask):
    app.register_blueprint(bp)
