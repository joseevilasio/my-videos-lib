from api.database import mongo
from api.plugins import (
    get_next_sequence_value,
    is_valid_url,
    returns_if_category_exists,
)

# CONTROLLER VIDEOS


def init_category():
    """Create free category if it doesn't exist"""

    query = mongo.db.category.find_one({"id": 1}, projection={"_id": False})

    if query is None:
        id = get_next_sequence_value("category")
        mongo.db.category.insert_one(
            {
                "id": id,  # insert auto increment
                "title": "livre",
                "color": "branco",
            }
        )


def get_all_videos() -> dict:
    """Get all videos from database and list information"""
    query = mongo.db.videos.find(projection={"_id": False})

    data = {}
    for video in query:
        data[f"{video['id']}"] = video

    if not data:
        raise FileNotFoundError("No videos found")

    return data


def get_video_by_id(video_id: int) -> dict:
    """Get video by id from database and list information"""

    query = mongo.db.videos.find_one(
        {"id": video_id}, projection={"_id": False}
    )

    if query is None:
        raise FileNotFoundError("Video not found")

    return query


def add_new_video(data: dict) -> int:
    """Add new video on database"""

    init_category()

    id = get_next_sequence_value("videos")

    if (
        data.get("title") is None
        or data.get("description") is None
        or data.get("url") is None
    ):
        raise ValueError("This field cannot be empty")

    if len(data["title"].replace(" ", "")) <= 0:
        raise ValueError("This field cannot be empty")

    if len(data["description"].replace(" ", "")) <= 0:
        raise ValueError("This field cannot be empty")

    if is_valid_url(data["url"]) is False:
        raise ValueError("Url is invalid")

    if data.get("categoryId") is None:
        data["categoryId"] = 1

    mongo.db.videos.insert_one(
        {
            "id": id,  # insert auto increment
            "title": data["title"],
            "description": data["description"],
            "url": data["url"],
            "categoryId": data["categoryId"],
        }
    )
    return id


def update_video(video_id: int, data) -> int:
    """Update video info on database"""

    query = mongo.db.videos.find_one(
        {"id": video_id}, projection={"_id": False}
    )

    if query is None:
        raise FileNotFoundError("Video not found")

    if data.get("title") is None:
        data["title"] = query["title"]
    if data.get("description") is None:
        data["description"] = query["description"]
    if data.get("url") is None:
        data["url"] = query["url"]
    if data.get("categoryId") is None:
        data["categoryId"] = query["categoryId"]

    mongo.db.videos.find_one_and_update({"id": video_id}, {"$set": data})
    return video_id


def delete_video(video_id: int) -> str:
    """Delete one video by id"""

    if mongo.db.videos.delete_one({"id": video_id}).deleted_count == 1:
        return "Video deleted"
    raise FileNotFoundError("Video not found")


def search_video(search: str) -> dict:
    """Search video by string match"""

    query = mongo.db.videos.find(
        filter={"$or": [{"title": {"$regex": rf"{search}", "$options": "i"}}]},
        projection={"_id": False},
    )

    data = {}
    for video in query:
        data[f"{video['id']}"] = video

    if not data:
        raise FileNotFoundError(f"No videos found with '{search}'")

    return data


# CONTROLLER CATEGORY


def get_all_category():
    """Get all category from database and list information"""

    query = mongo.db.category.find(projection={"_id": False})

    data = {}
    for category in query:
        data[f"{category['id']}"] = category

    if not data:
        raise FileNotFoundError("No videos found")

    return data


def get_category_by_id(categoryId: int):
    """Get category by id from database and list information"""

    query = mongo.db.category.find_one(
        {"id": categoryId}, projection={"_id": False}
    )

    if query is None:
        raise FileNotFoundError("Category not found")

    return query


def add_new_category(data: dict) -> int:
    """Add new category on database"""

    id = get_next_sequence_value("category")

    if data.get("title") is None or data.get("color") is None:
        raise ValueError("This field cannot be empty")

    if len(data["title"].replace(" ", "")) <= 0:
        raise ValueError("This field cannot be empty")

    if returns_if_category_exists(data["title"]):
        raise ValueError("Category already exists")

    if len(data["color"].replace(" ", "")) <= 0:
        raise ValueError("This field cannot be empty")

    mongo.db.category.insert_one(
        {
            "id": id,  # insert auto increment
            "title": data["title"],
            "color": data["color"],
        }
    )

    return id


def update_category(categoryId: int, data: dict) -> int:
    """Update category info on database"""

    query = mongo.db.category.find_one(
        {"id": categoryId}, projection={"_id": False}
    )

    if query is None:
        raise FileNotFoundError("Category not found")

    if data.get("title") is None:
        data["title"] = query["title"]
    if data.get("color") is None:
        data["color"] = query["color"]

    mongo.db.category.find_one_and_update({"id": categoryId}, {"$set": data})
    return categoryId


def delete_category(categoryId: int):
    """Delete one category by id"""

    if mongo.db.category.delete_one({"id": categoryId}).deleted_count == 1:
        return f"Category {categoryId} deleted"
    raise FileNotFoundError("Category not found")


# CONTROLLER RELATIONSHIP


def get_all_videos_by_category(categoryId: int):
    """Get all videos by category from database and list information"""

    query = mongo.db.videos.find(
        {"categoryId": f"{categoryId}"}, projection={"_id": False}
    )

    data = {}
    for video in query:
        data[f"{video['categoryId']}"] = video

    if not data:
        raise FileNotFoundError("No videos found")

    return data
