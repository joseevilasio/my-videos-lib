import json

import pytest

from api.auth import create_user
from api.controller import add_new_category, add_new_video
from api.database import mongo
from api.plugins import convert_json_for_dict
from tests.constants import CATEGORY_FILE, VIDEO_FILE, VIDEO_FILE_2


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
def test_positive_list_videos(client):
    """Test to check if list videos route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    add_new_video(convert_json_for_dict(VIDEO_FILE))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/videos", headers=headers)
    assert response.status_code == 200


@pytest.mark.integration
def test_negative_list_videos(client):
    """Test negative to check if list videos route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/videos", headers=headers)
    assert response.status_code == 404


@pytest.mark.integration
def test_one_video_positive_data(client):
    """Test to check if one video route is return 404"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    add_new_video(convert_json_for_dict(VIDEO_FILE))
    add_new_video(convert_json_for_dict(VIDEO_FILE_2))

    response_1 = client.get("/videos/1", headers=headers)
    response_2 = client.get("/videos/2", headers=headers)

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert b"Git e Github para iniciantes" in response_1.data
    assert b"https://www.youtube.com/watch?v=8485663" in response_2.data


@pytest.mark.integration
def test_one_video_negative_data(client):
    """Test negative to check if one video route is return 404"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response_1 = client.get("/videos/1", headers=headers)
    response_2 = client.get("/videos/2", headers=headers)

    assert response_1.status_code == 404
    assert response_2.status_code == 404


@pytest.mark.integration
def test_positive_delete_one_video(client):
    """Test to check if delete one video route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    response_delete = client.delete("/videos/1", headers=headers)
    response_get = client.get("/videos/1", headers=headers)

    assert response_delete.status_code == 200
    assert response_get.status_code == 404


@pytest.mark.integration
def test_negative_delete_one_video(client):
    """Test negative to check if delete one video route is return 404"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response_delete = client.delete("/videos/1", headers=headers)

    assert response_delete.status_code == 404


@pytest.mark.integration
def test_positive_new_video(client):
    """Test to check if new video route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    with open(VIDEO_FILE, "r") as content:
        response = client.post(
            "/videos/new",
            json=json.load(content),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        assert response.status_code == 200
        assert b"Redirecting" in response.data
        assert response.headers["Location"] == "/videos/1"


@pytest.mark.integration
def test_positive_update_data_video(client):
    """Test to check if update video route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
    assert insert_data == 1

    data = {"title": "Aprenda GIT/GITHUB em 15 minutos"}

    response = client.put(
        "/videos/1",
        json=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200
    assert b"Redirecting" in response.data
    assert response.headers["Location"] == "/videos/1"


@pytest.mark.integration
def test_positive_search_video_query(client):
    """Test to check if search video route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
    assert insert_data == 1

    headers = {"Authorization": f"Bearer {token}"}

    word = "github"

    response = client.get(f"/videos/?search={word}", headers=headers)

    assert response.status_code == 200
    assert (
        b"Aprenda a usar o Git e Github com os cursos da Alura"
        in response.data
    )


@pytest.mark.integration
def test_negative_search_video_query(client):
    """Test to check if search video route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
    assert insert_data == 1

    headers = {"Authorization": f"Bearer {token}"}

    word = "carro"

    response = client.get(f"/videos/?search={word}", headers=headers)
    print(response.data)

    assert response.status_code == 404


# CATEGORY TEST


@pytest.mark.integration
def test_positive_list_category(client):
    """Test to check if list category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    add_new_category(convert_json_for_dict(CATEGORY_FILE))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/category", headers=headers)
    assert response.status_code == 200


@pytest.mark.integration
def test_negative_list_category(client):
    """Test negative to check if list category route is return 404"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/category", headers=headers)
    assert response.status_code == 404


@pytest.mark.integration
def test_positive_one_category_data(client):
    """Test to check if one category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    add_new_category(convert_json_for_dict(CATEGORY_FILE))

    response = client.get("/category/1", headers=headers)

    assert response.status_code == 200
    assert b"Humor" in response.data


@pytest.mark.integration
def test_negative_one_category_data(client):
    """Test negative to check if one category route is return 404"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/category/1", headers=headers)

    assert response.status_code == 404


@pytest.mark.integration
def test_positive_delete_one_category(client):
    """Test to check if delete one category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    add_new_category(convert_json_for_dict(CATEGORY_FILE))

    response_delete = client.delete("/category/1", headers=headers)
    response_get = client.get("/category/1", headers=headers)

    assert response_delete.status_code == 200
    assert response_get.status_code == 404


@pytest.mark.integration
def test_negative_delete_one_category(client):
    """Test negative to check if delete one category route is return 404"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    headers = {"Authorization": f"Bearer {token}"}

    response_delete = client.delete("/category/1", headers=headers)

    assert response_delete.status_code == 404


@pytest.mark.integration
def test_positive_new_category(client):
    """Test to check if new category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    with open(CATEGORY_FILE, "r") as content:
        response = client.post(
            "/category/new",
            json=json.load(content),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        assert response.status_code == 200
        assert b"Redirecting" in response.data
        assert response.headers["Location"] == "/category/1"


@pytest.mark.integration
def test_positive_update_data_category(client):
    """Test to check if update category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    insert_data = add_new_category(convert_json_for_dict(CATEGORY_FILE))
    assert insert_data == 1

    headers = {"Authorization": f"Bearer {token}"}

    data = {"title": "Terror"}

    response = client.put("/category/1", json=data, headers=headers)

    assert response.status_code == 200
    assert b"Redirecting" in response.data
    assert response.headers["Location"] == "/category/1"


@pytest.mark.integration
def test_positive_show_videos_by_category(client):
    """Test to check if show videos by category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    insert_category = add_new_category(convert_json_for_dict(CATEGORY_FILE))
    insert_video = add_new_video(convert_json_for_dict(VIDEO_FILE))

    assert insert_category == 1
    assert insert_video == 1

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/category/1/videos", headers=headers)

    assert response.status_code == 200
    assert b"Git e Github para iniciantes" in response.data


@pytest.mark.integration
def test_negative_show_videos_by_category(client):
    """Test to check if show videos by category route is return OK"""

    create_user(username="admin", password="123456")
    token = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["token"]

    insert_category = add_new_category(convert_json_for_dict(CATEGORY_FILE))

    assert insert_category == 1

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/category/1/videos", headers=headers)

    assert response.status_code == 404
