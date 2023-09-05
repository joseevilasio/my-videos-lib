import re

from api.database import mongo


def get_next_sequence_value(db_name):
    sequence = mongo.db.sequences.find_one_and_update(
        {"_id": db_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return sequence["sequence_value"]


def is_valid_url(url):
    # Expressão regular para verificar o formato básico da URL
    url_pattern = re.compile(
        r"^(https?://)?"  # Protocolo (opcional)
        r"([A-Za-z_0-9.-]+)"  # Nome de host (obrigatório)
        r"(:\d+)?"  # Porta (opcional)
        r"(/[^?#]*)?"  # Caminho (opcional)
        r"(\?[^#]*)?"  # Query string (opcional)
        r"(#.*)?$"  # Fragmento (opcional)
    )

    # Verificar se a URL corresponde ao padrão
    return bool(url_pattern.match(url))


def get_all_videos():
    """Get all videos from database and list information"""
    query = mongo.db.videos.find(projection={"_id": False})
    data = {}
    for video in query:
        data[f"{video['id']}"] = video
    return data


def get_video_by_id(video_id: int):
    """Get video by id from database and list information"""

    query = mongo.db.videos.find_one(
        {"id": video_id}, projection={"_id": False}
    )
    if query is None:
        raise FileExistsError("Video not found")
    return query


def add_new_video(data: dict):
    """Add new video on database"""
    id = get_next_sequence_value("videos")

    if len(data["title"].replace(" ", "")) <= 0:
        raise FileExistsError("This field cannot be empty")

    if len(data["description"].replace(" ", "")) <= 0:
        raise FileExistsError("This field cannot be empty")

    if is_valid_url(data["url"]) is False:
        raise ValueError("Url is invalid")

    mongo.db.videos.insert_one(
        {
            "id": id,  # insert auto increment
            "title": data["title"],
            "description": data["description"],
            "url": data["url"],
        }
    )

    return id


def update_video(video_id: int, data):
    """Update video info on database"""

    query = mongo.db.videos.find_one(
        {"id": video_id}, projection={"_id": False}
    )
    if query is None:
        raise FileExistsError("Video not found")

    if data.get("title") is None:
        data["title"] = query["title"]
    if data.get("description") is None:
        data["description"] = query["description"]
    if data.get("url") is None:
        data["url"] = query["url"]
    mongo.db.videos.find_one_and_update({"id": video_id}, {"$set": data})
    return video_id


def delete_video(video_id: int):
    """Delete one video by id"""

    if mongo.db.videos.delete_one({"id": video_id}).deleted_count == 1:
        return f"Video {video_id} deleted"
    raise FileExistsError("Video not found")


# Category


# def get_all_category():
#     """Get all category from database and list information"""

#     with get_session() as session:
#         query = session.exec(select(Category)).fetchall()
#         if query:
#             results = [category.to_dict() for category in query]
#         else:
#             return None

#     return jsonify(results)


# def get_category_by_id(category_id):
#     """Get category by id from database and list information"""

#     with get_session() as session:
#         query = session.exec(
#             select(Category).where(Category.id == category_id)
#         ).first()
#         if query:
#             results = query.to_dict()
#         else:
#             return None

#     return jsonify(results)


# def add_new_category(data):
#     """Add new category on database"""

#     with open(data, encoding="utf-8") as data_json:
#         _data = json.load(data_json)

#     with get_session() as session:
#         if type(_data) == list:
#             for item in _data:
#                 new = Category(**item)
#                 session.add(new)

#         elif type(_data) == dict:
#             new = Category(**_data)
#             session.add(new)

#         session.commit()

#     return "created with success"


# def update_category(category_id, data):
#     """Update category info on database"""

#     with get_session() as session:
#         category = session.exec(
#             select(Category).where(Category.id == category_id)
#         ).one()
#         data_dict = json.loads(data)

#         for key, value in data_dict.items():
#             if key == "title":
#                 category.title = value
#             if key == "color":
#                 category.color = value

#         session.commit()

#     return "updated with success"


# def delete_category(category_id=None):
#     """Delete one category by id or all categorys on database"""

#     with get_session() as session:
#         query = session.exec(
#             select(Category).where(Category.id == category_id)
#         ).one()
#         session.delete(query)
#         session.commit()

#     return "delete success"
