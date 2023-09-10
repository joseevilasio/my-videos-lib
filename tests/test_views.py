import pytest

from api.controller import add_new_video
from api.plugins import convert_json_for_dict
from tests.constants import VIDEO_FILE, VIDEO_FILE_2


@pytest.mark.integration
def test_index_positive(client):
    """Test to check if index route is return OK"""

    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World! MyVideosLIB API" in response.data


@pytest.mark.integration
def test_route_negative(client):
    """Negative test to check if the non-existent
    route is returning Not Found"""

    response = client.get("/fake_route")
    assert response.status_code == 404


@pytest.mark.integration
def test_list_videos_positive(client):
    """Test to check if list videos route is return OK"""

    data = convert_json_for_dict(VIDEO_FILE)
    insert_video = add_new_video(data)

    response = client.get("/videos")
    assert insert_video is not None
    assert response.status_code == 200


@pytest.mark.integration
def test_one_video_positive_data(client):
    """Test to check if one video route is return OK"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))
    add_new_video(convert_json_for_dict(VIDEO_FILE_2))

    response_1 = client.get("/videos/1")
    response_2 = client.get("/videos/2")

    assert response_1.status_code == 200
    assert response_1.status_code == 200
    assert b"Git e Github para iniciantes" in response_1.data
    assert b"https://www.youtube.com/watch?v=8485663" in response_2.data


@pytest.mark.integration
def test_delete_one_video(client):
    """Test to check if delete one video route is return OK"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    response_delete = client.delete("/videos/1")
    response_get = client.get("/videos/1")

    assert response_delete.status_code == 200
    assert response_get.status_code == 404


# @pytest.mark.integration
# def test_new_video(client):
#     """Test to check if new video route is return OK"""

#     response = client.post(
#         "/videos/new",
#         json=VIDEO_FILE,
#         headers={"Content-Type": "application/json"}
#     )

#     assert response.status_code == 200
#     assert b"1" in response.data


# def test_update_data_video(client):
#     """Test to check if update video route is return OK"""

#     insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
#     assert insert_data == 1

#     data = {"title": "Aprenda GIT/GITHUB em 15 minutos"}

#     response = client.put("/videos/1", json=json.dumps(data))

#     assert response.status_code == 200
#     assert b"Aprenda GIT/GITHUB em 15 minutos" in response.data


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
