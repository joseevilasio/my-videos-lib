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
    return result_query    


def add_new_video(**data):
    """Add new video on database"""
    video = dict(
        {
            "title": data["title"],
            "description": data["description"],
            "url": data["url"],
        }
    )
    conn.exec_driver_sql(
        """\
        INSERT INTO video (title, description , url)
        VALUES (:title, :description, :url);
        """,
        video,
    )
    conn.commit()

    return "created with success"


def update_video(video_id, **data):
    """Update video info on database"""

    video = dict(
        {
            "title": data["title"],
            "description": data["description"],
            "url": data["url"],
        }
    )

    for key, value in video.items():
        if value:
            conn.exec_driver_sql(
                """\
            UPDATE video
            SET {column} = {value}
            WHERE id = {id};
            """.format(
                    column=key, value=(f"'{value}'"), id=video_id
                )
            )

    conn.commit()

    return "updated with success"


def delete_video(video_id=None):
    """Delete one video by id or all videos on database"""
    conn.exec_driver_sql(f"DELETE FROM video WHERE id={video_id};")
    conn.commit()
    return "delete success"
