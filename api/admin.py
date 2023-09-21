from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib.pymongo import ModelView
from flask_simplelogin import login_required
from wtforms import fields, form, validators

from api.database import mongo
from api.plugins import get_next_sequence_value

# decorate Flask-Admin view via Monkey Patching
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
ModelView._handle_view = login_required(ModelView._handle_view)


class VideosForm(form.Form):
    title = fields.StringField("Title", [validators.data_required()])
    description = fields.TextAreaField(
        "Description", [validators.data_required()]
    )
    url = fields.URLField("url", [validators.url()])
    categoryId = fields.IntegerField("CategoryId")
    id = fields.HiddenField("id")


class CategoryForm(form.Form):
    title = title = fields.StringField("Title", [validators.data_required()])
    color = fields.TextAreaField("Color", [validators.data_required()])
    id = fields.HiddenField("id")


class AdminVideos(ModelView):
    column_list = ("id", "title", "url", "categoryId")
    form = VideosForm

    def on_model_change(self, form, video, is_created):
        if is_created:
            video["id"] = get_next_sequence_value("videos")


class AdminCategory(ModelView):
    column_list = ("id", "title", "color")
    form = CategoryForm

    def on_model_change(self, form, category, is_created):
        if is_created:
            category["id"] = get_next_sequence_value("category")


def configure(app):
    """Init app on Flask-Admin"""
    app.admin = Admin(
        app,
        name=app.config.get("TITLE"),
        template_mode=app.config.get(
            "FLASK_ADMIN_TEMPLATE_MODE", "bootstrap4"
        ),
    )
    app.admin.add_view(AdminVideos(mongo.db.videos, "Videos"))
    app.admin.add_view(AdminCategory(mongo.db.category, "Category"))
