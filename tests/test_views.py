# from flask import json

# from api.controller import add_new_video
# from tests.constants import VIDEO_FILE, VIDEO_FILE_2


# def test_index_positive(client):
#     """Test to check if index route is return OK"""

#     response = client.get("/")
#     assert response.status_code == 200
#     assert b"Hello, World! MyVideosLIB API" in response.data


# def test_route_negative(client):
#     """Negative test to check if the non-existent
#     route is returning Not Found"""

#     response = client.get("/fake_route")
#     assert response.status_code == 404


# def test_list_videos_positive(client):
#     """Test to check if list videos route is return OK"""

#     add_new_video(VIDEO_FILE)

#     with get_session() as session:
#         result = session.exec(select(Video)).first()

#     response = client.get("/videos")
#     assert result is not None
#     assert response.status_code == 200


# def test_one_video_positive_data(client):
#     """Test to check if one video route is return OK"""

#     with get_session() as session:
#         add_new_video(VIDEO_FILE)
#         add_new_video(VIDEO_FILE_2)

#         result = session.exec(select(Video)).first()

#         response_1 = client.get("/videos/1")
#         response_2 = client.get("/videos/2")

#         assert result is not None
#         assert response_1.status_code == 200
#         assert response_1.status_code == 200
#         assert b"Git e Github para iniciantes" in response_1.data
#         assert b"https://www.youtube.com/watch?v=8485663" in response_2.data


# def test_delete_one_video(client):
#     """Test to check if delete one video route is return OK"""

#     with get_session() as session:
#         add_new_video(VIDEO_FILE)

#         result_after = session.exec(select(Video)).first()
#         assert result_after is not None

#         response_delete = client.delete("/videos/1")
#         response_get = client.get("/videos/1")

#         result_before = session.exec(select(Video)).first()

#         assert result_before is None
#         assert response_delete.status_code == 200
#         assert response_get.status_code == 404


# def test_new_video(client):
#     """Test to check if new video route is return OK"""

#     with get_session() as session:
#         response_post = client.post("/videos/new", json=VIDEO_FILE)
#         response_get = client.get("/videos/1")

#         result_before = session.exec(select(Video)).first()

#         assert result_before is not None
#         assert response_post.status_code == 200
#         assert response_get.status_code == 200
#         assert b"https://www.youtube.com/watch?v=ABC123" in response_get.data


# def test_update_data_video(client):
#     """Test to check if update video route is return OK"""

#     with get_session() as session:
#         add_new_video(VIDEO_FILE)
#         result_after = session.exec(select(Video)).first()
#         assert result_after is not None

#         data = {
#             "title": "Aprenda GIT/GITHUB em 15 minutos",
#             "description": """Aprenda a usar o Git e Github com os cursos da
#             Alura""",
#             "url": "https://www.youtube.com/watch?v=ABC123",
#         }

#         response_put = client.put("/videos/1", json=json.dumps(data))

#         result_before = session.exec(select(Video.title)).first()

#         assert result_before == "Aprenda GIT/GITHUB em 15 minutos"
#         assert response_put.status_code == 200
#         assert b"updated with success" in response_put.data


# def test_update_partial_video(client):
#     """Test to check if update partial video route is return OK"""

#     with get_session() as session:
#         add_new_video(VIDEO_FILE)
#         result_after = session.exec(select(Video)).first()
#         assert result_after is not None

#         data = {
#             "title": "Aprenda GIT/GITHUB em 15 minutos",
#         }

#         response_patch = client.patch("/videos/1", json=json.dumps(data))

#         result_before = session.exec(select(Video.title)).first()

#         assert result_before == "Aprenda GIT/GITHUB em 15 minutos"
#         assert response_patch.status_code == 200
#         assert b"updated with success" in response_patch.data