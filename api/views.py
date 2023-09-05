from flask import (
    Blueprint,
    Flask,
    abort,
    jsonify,
    redirect,
    request,
    url_for,
)

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


@bp.route("/videos/new", methods=["POST", "GET"])
def new_video():
    data = request.get_json()
    video = add_new_video(data)
    return redirect(url_for("api.one_video", video_id=video))


@bp.route("/videos/<int:video_id>", methods=["PUT", "GET"])
def update_data_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return redirect(url_for("api.one_video", video_id=video))


@bp.route("/videos/<int:video_id>", methods=["PATCH", "GET"])
def update_partial_video(video_id):
    data = request.get_json()
    video = update_video(video_id, data)
    return redirect(url_for("api.one_video", video_id=video))


# Category routes


# @bp.route("/category")
# def list_category():
#     category = get_all_category()
#     if not category:
#         return abort(404)
#     return category


# @bp.route("/category/<int:category_id>")
# def one_category(category_id):
#     category = get_category_by_id(category_id)
#     if not category:
#         return abort(404)
#     return category


# @bp.route("/category/<int:category_id>", methods=["DELETE"])
# def delete_one_category(category_id):
#     category = get_category_by_id(category_id)
#     if not category:
#         return abort(404)
#     else:
#         exec_category = delete_category(category_id)
#         return exec_category


# @bp.route("/category/new", methods=["POST", "GET"])
# def new_category():
#     data = request.get_json()
#     category = add_new_category(data)
#     return category


# @bp.route("/category/<int:category_id>", methods=["PUT", "GET"])
# def update_data_category(category_id):
#     data = request.get_json()
#     category = update_video(category_id, data)
#     return category


# @bp.route("/category/<int:category_id>", methods=["PATCH", "GET"])
# def update_partial_category(category_id):
#     data = request.get_json()
#     category = update_category(category_id, data)
#     return category


def configure(app: Flask):
    app.register_blueprint(bp)
