from api.database import conn


def get_all_videos():
    """Get all videos from database and list information"""

    fields = ("id", "title", "description", "url")
    query = conn.exec_driver_sql("SELECT * FROM video;")
    results = [dict(zip(fields, video)) for video in query]
    # Atenção para serializar para json
    return results


def get_video_by_id(video_id):
    """Get video by id from database and list information"""

    fields = ("id", "title", "description", "url")
    query = conn.exec_driver_sql(f"SELECT * FROM video WHERE id = {video_id};")
    result_query = [dict(zip(fields, video)) for video in query]
    if result_query:
        return result_query
    else:
        return f"not found: {video_id}"


def add_new_video(title, description, url):
    """Add new video on database"""
    video = dict(
            {"title": title,
             "description": description,
             "url": url,
             })

    query = conn.exec_driver_sql(
        """\
        INSERT INTO video (title, description , url)
        VALUES (:title, :description, :url);
        """,
        video,
    )
    
    conn.commit()

    return "created with success"

def update_video():
    """Update video infor on database"""
    ...


def delete_video(video_id=None):
    """Delete one video by id or all videos on database"""
    ...
