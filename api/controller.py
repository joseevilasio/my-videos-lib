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


def regex_case_insensitive(word):
    return re.compile(f"^{re.escape(word)}$", re.IGNORECASE)


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


def search_video(search: str):
    """Search video by string match"""
    # TODO: Resolver problema de exibição, return vazio
    # TODO: regex funciona com texto exatamente igual
    query = mongo.db.videos.find(
        filter={"title": {"$regex": f"{search}"}}, projection={"_id": False}
    )
    print(list(query))

    if query is None:
        raise FileExistsError(f"Video not found with '{search}'")
    
    data = {}
    for video in query:
        data[f"{video['id']}"] = video
    return data


# CATEGORY


def get_all_category():
    """Get all category from database and list information"""

    query = mongo.db.category.find(projection={"_id": False})
    data = {}
    for category in query:
        data[f"{category['id']}"] = category
    
    return data


def get_category_by_id(category_id: int):
    """Get category by id from database and list information"""

    query = mongo.db.category.find_one(
        {"id": category_id}, projection={"_id": False}
    )
    if query is None:
        raise FileExistsError("Category not found")
    return query


def add_new_category(data: dict):
    """Add new category on database"""

    id = get_next_sequence_value("category")

    if len(data["title"].replace(" ", "")) <= 0:
        raise FileExistsError("This field cannot be empty")

    if len(data["color"].replace(" ", "")) <= 0:
        raise FileExistsError("This field cannot be empty")

    mongo.db.category.insert_one(
        {
            "id": id,  # insert auto increment
            "title": data["title"],
            "color": data["color"],
        }
    )

    return id


def update_category(category_id: int, data: dict):
    """Update category info on database"""

    query = mongo.db.category.find_one(
        {"id": category_id}, projection={"_id": False}
    )
    if query is None:
        raise FileExistsError("Category not found")

    if data.get("title") is None:
        data["title"] = query["title"]
    if data.get("color") is None:
        data["color"] = query["color"]

    mongo.db.category.find_one_and_update({"id": category_id}, {"$set": data})
    return category_id


def delete_category(category_id: int):
    """Delete one category by id"""

    if mongo.db.category.delete_one({"id": category_id}).deleted_count == 1:
        return f"Video {category_id} deleted"
    raise FileExistsError("Category not found")
