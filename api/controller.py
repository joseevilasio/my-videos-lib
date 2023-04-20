from flask import json, jsonify
from sqlmodel import select

from api.database import get_session
from api.model import Category, Video


def get_all_videos():
    """Get all videos from database and list information"""

    with get_session() as session:
        query = session.exec(select(Video)).fetchall()
        if query:
            results = [video.to_dict() for video in query]
        else:
            return None

    return jsonify(results)


def get_video_by_id(video_id):
    """Get video by id from database and list information"""

    with get_session() as session:
        query = session.exec(select(Video).where(Video.id == video_id)).first()
        if query:
            results = query.to_dict()
        else:
            return None

    return jsonify(results)


def add_new_video(data):
    """Add new video on database"""

    with open(data, encoding="utf-8") as data_json:
        _data = json.load(data_json)

    with get_session() as session:
        if type(_data) == list:
            for item in _data:
                new = Video(**item)
                session.add(new)

        elif type(_data) == dict:
            new = Video(**_data)
            session.add(new)

        session.commit()

    return "created with success"


def update_video(video_id, data):
    """Update video info on database"""

    with get_session() as session:
        video = session.exec(select(Video).where(Video.id == video_id)).one()
        data_dict = json.loads(data)

        for key, value in data_dict.items():
            if key == "title":
                video.title = value
            if key == "description":
                video.description = value
            if key == "url":
                video.url = value

        session.commit()

    return "updated with success"


def delete_video(video_id=None):
    """Delete one video by id or all videos on database"""

    with get_session() as session:
        query = session.exec(select(Video).where(Video.id == video_id)).one()
        session.delete(query)
        session.commit()

    return "delete success"


# Category


def get_all_category():
    """Get all category from database and list information"""

    with get_session() as session:
        query = session.exec(select(Category)).fetchall()
        if query:
            results = [category.to_dict() for category in query]
        else:
            return None

    return jsonify(results)


def get_category_by_id(category_id):
    """Get category by id from database and list information"""

    with get_session() as session:
        query = session.exec(
            select(Category).where(Category.id == category_id)
        ).first()
        if query:
            results = query.to_dict()
        else:
            return None

    return jsonify(results)


def add_new_category(data):
    """Add new category on database"""

    with open(data, encoding="utf-8") as data_json:
        _data = json.load(data_json)

    with get_session() as session:
        if type(_data) == list:
            for item in _data:
                new = Category(**item)
                session.add(new)

        elif type(_data) == dict:
            new = Category(**_data)
            session.add(new)

        session.commit()

    return "created with success"


def update_category(category_id, data):
    """Update category info on database"""

    with get_session() as session:
        category = session.exec(
            select(Category).where(Category.id == category_id)
        ).one()
        data_dict = json.loads(data)

        for key, value in data_dict.items():
            if key == "title":
                category.title = value
            if key == "color":
                category.color = value

        session.commit()

    return "updated with success"


def delete_category(category_id=None):
    """Delete one category by id or all categorys on database"""

    with get_session() as session:
        query = session.exec(
            select(Category).where(Category.id == category_id)
        ).one()
        session.delete(query)
        session.commit()

    return "delete success"
