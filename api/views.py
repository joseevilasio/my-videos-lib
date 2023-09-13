from flask import Blueprint, Flask, abort, jsonify, redirect, request, url_for
from flask_jwt_extended import jwt_required

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
@jwt_required()
def list_videos():
    try:
        videos = get_all_videos()
    except FileNotFoundError:
        return abort(404)
    return jsonify(videos), 200


@bp.route("/videos/<int:video_id>")
@jwt_required()
def one_video(video_id):
    try:
        video = get_video_by_id(video_id)
    except FileNotFoundError:
        return abort(404)
    return jsonify(video), 200


@bp.route("/videos/<int:video_id>", methods=["DELETE"])
@jwt_required()
def delete_one_video(video_id):
    try:
        get_video_by_id(video_id)
    except FileNotFoundError:
        return abort(404)
    else:
        exec_video = delete_video(video_id)
        return exec_video


@bp.route("/videos/new", methods=["POST"])
@jwt_required()
def new_video():
    data = request.get_json()   
    video = add_new_video(data)   

    return redirect(url_for("api.one_video", video_id=video)), 200


@bp.route("/videos/<int:video_id>", methods=["PUT"])
@jwt_required()
def update_data_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return redirect(url_for("api.one_video", video_id=video)), 200


@bp.route("/videos/")
@jwt_required()
def search_video_query():
    search = request.args.get("search")

    try:
        videos = search_video(search)
    except FileNotFoundError:
        return abort(404)
    return jsonify(videos), 200


# CATEGORY ROUTES


@bp.route("/category")
@jwt_required()
def list_category():
    try:
        category = get_all_category()
    except FileNotFoundError:
        return abort(404)
    return jsonify(category), 200


@bp.route("/category/<int:categoryId>")
@jwt_required()
def one_category(categoryId):
    try:
        category = get_category_by_id(categoryId)
    except FileNotFoundError:
        return abort(404)
    return jsonify(category), 200


@bp.route("/category/<int:categoryId>", methods=["DELETE"])
@jwt_required()
def delete_one_category(categoryId):
    try:
        get_category_by_id(categoryId)
    except FileNotFoundError:
        return abort(404)
    else:
        exec_category = delete_category(categoryId)
        return exec_category


@bp.route("/category/new", methods=["GET", "POST"])
@jwt_required()
def new_category():
    data = request.get_json()
    category = add_new_category(data)
    return redirect(url_for("api.one_category", categoryId=category), 200)


@bp.route("/category/<int:categoryId>", methods=["GET", "PUT"])
@jwt_required()
def update_data_category(categoryId):
    data = request.get_json()
    category = update_category(categoryId, data)
    return redirect(url_for("api.one_category", categoryId=category), 200)


# RELATIONSHIP


@bp.route("/category/<int:categoryId>/videos", methods=["GET"])
@jwt_required()
def show_videos_by_category(categoryId):
    try:
        videos_category = get_all_videos_by_category(categoryId)
    except FileNotFoundError:
        return abort(404)
    return jsonify(videos_category), 200


def configure(app: Flask):
    app.register_blueprint(bp)
