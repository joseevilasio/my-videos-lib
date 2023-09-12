import pytest

from api.controller import (
    add_new_category,
    add_new_video,
    delete_category,
    delete_video,
    get_all_category,
    get_all_videos,
    get_all_videos_by_category,
    get_category_by_id,
    get_video_by_id,
    search_video,
    update_category,
    update_video,
)
from api.plugins import convert_json_for_dict
from tests.constants import (
    VIDEO_FILE,
    VIDEO_FILE_2,
    VIDEO_FILE_3_ERRO,
    VIDEO_FILE_4_ERRO,
    VIDEO_FILE_5_ERRO,
)


class MockMongoDb:
    def insert_one(self, data):
        raise SystemError()


@pytest.mark.unit
def test_get_all_videos_positive():
    """Test get all videos from database and list information"""

    data = convert_json_for_dict(VIDEO_FILE)

    with pytest.raises(FileNotFoundError):
        get_all_videos() == {}

    insert_data = add_new_video(data)
    result = get_all_videos()

    assert insert_data == 1
    assert result["1"]["title"] == "Git e Github para iniciantes"


@pytest.mark.unit
def test_get_all_videos_negative():
    """Test negative get all videos from database and list information"""

    with pytest.raises(FileNotFoundError):
        get_all_videos()


@pytest.mark.unit
def test_get_video_by_id_positive():
    """Test positive get video by id from database and list information"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))
    add_new_video(convert_json_for_dict(VIDEO_FILE_2))

    result_1 = get_video_by_id(1)
    result_2 = get_video_by_id(2)

    assert result_1["title"] == "Git e Github para iniciantes"
    assert result_2["title"] == "Introdução à programação em Go"


@pytest.mark.unit
@pytest.mark.parametrize("id", [3, 4])
def test_get_video_by_id_negative(id):
    """Test negative get video by id from database and list information"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))
    add_new_video(convert_json_for_dict(VIDEO_FILE_2))

    with pytest.raises(FileNotFoundError):
        get_video_by_id(id)


@pytest.mark.unit
def test_add_new_video_positive():
    """Test positive Add new video on database"""

    result_1 = add_new_video(convert_json_for_dict(VIDEO_FILE))
    result_2 = add_new_video(convert_json_for_dict(VIDEO_FILE_2))

    assert result_1 == 1
    assert result_2 == 2


@pytest.mark.unit
def test_add_new_video_negative_untitled():
    """Test negative Add new video on database"""

    data = convert_json_for_dict(VIDEO_FILE_3_ERRO)

    with pytest.raises(ValueError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_without_description():
    """Test negative Add new video on database"""

    data = convert_json_for_dict(VIDEO_FILE_4_ERRO)

    with pytest.raises(ValueError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_without_url():
    """Test negative Add new video on database"""

    data = convert_json_for_dict(VIDEO_FILE_5_ERRO)

    with pytest.raises(ValueError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_title_empty():
    """Test negative Add new video on database"""

    data = {
        "title": "  ",
        "description": "Aprenda a usar o Git e Github com os cursos da Alura",
        "url": "https://www.youtube.com/watch?v=ABC123",
        "categoryId": "1",
    }

    with pytest.raises(ValueError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_description_empty():
    """Test negative Add new video on database"""

    data = {
        "title": "Git e Github para iniciantes",
        "description": " ",
        "url": "https://www.youtube.com/watch?v=ABC123",
        "categoryId": "1",
    }

    with pytest.raises(ValueError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_url_wrong():
    """Test negative Add new video on database"""

    data = {
        "title": "Git e Github para iniciantes",
        "description": "Aprenda a usar o Git e Github com os cursos da Alura",
        "url": "youtube com/watch?v=ABC123",
        "categoryId": "1",
    }

    with pytest.raises(ValueError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_positve_without_category():
    """Test negative Add new video on database"""

    data = {
        "title": "Git e Github para iniciantes",
        "description": "Aprenda a usar o Git e Github com os cursos da Alura",
        "url": "youtube.com/watch?v=ABC123",
    }

    assert add_new_video(data) == 1
    assert get_video_by_id(1).get("categoryId") is None


@pytest.mark.unit
def test_delete_video_positive():
    """test delete one video by id"""

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))

    assert insert_data == 1
    result = delete_video(1)
    assert result == "Video deleted"


@pytest.mark.unit
def test_delete_video_negative():
    """test delete one video by id"""

    with pytest.raises(FileNotFoundError):
        delete_video(1)


@pytest.mark.unit
def test_search_video_positive():
    """test search video by string match"""

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
    assert insert_data == 1

    word = "iniciantes"
    result = search_video(word)
    assert result["1"]["title"] == "Git e Github para iniciantes"


@pytest.mark.unit
def test_search_video_negative():
    """test search video by string match"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))
    word = "tempo"

    with pytest.raises(FileNotFoundError):
        search_video(word)


@pytest.mark.unit
def test_update_video_positive():
    """test update video info on database"""

    data = convert_json_for_dict(VIDEO_FILE)
    insert_data = add_new_video(data)

    assert insert_data == 1

    new_data = {"title": "Novos Rumos"}

    update_data = update_video(1, new_data)

    assert update_data == 1
    assert get_video_by_id(1)["title"] == "Novos Rumos"


@pytest.mark.unit
def test_update_video_positive_without_title():
    """test update video info on database"""

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
    assert insert_data == 1

    new_data = {"description": "Um novo olhar sobre as estruturas de dados"}

    update_data = update_video(1, new_data)

    assert update_data == 1
    assert (
        get_video_by_id(1)["description"]
        == "Um novo olhar sobre as estruturas de dados"
    )


@pytest.mark.unit
def test_update_video_negative():
    """test update video info on database"""

    insert_data = add_new_video(convert_json_for_dict(VIDEO_FILE))
    assert insert_data == 1

    new_data = {"title": "Novos Rumos"}

    with pytest.raises(FileNotFoundError):
        update_video(2, new_data)


# CATEGORY TEST


@pytest.mark.unit
def test_get_all_category_positive():
    """Test get all category from database and list information"""

    data = {"title": "Humor", "color": "blue"}

    insert_data = add_new_category(data)
    result = get_all_category()

    assert insert_data == 1
    assert result["1"]["title"] == "Humor"


@pytest.mark.unit
def test_get_all_category_negative():
    """Test negative get all category from database and list information"""

    with pytest.raises(FileNotFoundError):
        get_all_category()


@pytest.mark.unit
def test_get_category_by_id_positive():
    """Test positive get category by id from database and list information"""

    data = {"title": "Humor", "color": "blue"}

    add_new_category(data)

    result = get_category_by_id(1)

    assert result != FileNotFoundError
    assert result["title"] == "Humor"


@pytest.mark.unit
def test_get_category_by_id_negative():
    """Test negative get category by id from database and list information"""

    data = {"title": "Humor", "color": "blue"}

    add_new_category(data)

    with pytest.raises(FileNotFoundError):
        get_category_by_id(2)


@pytest.mark.unit
def test_add_new_category_positive():
    """Test positive Add new category on database"""

    data = {"title": "Humor", "color": "blue"}

    result = add_new_category(data)

    assert result == 1


@pytest.mark.unit
def test_add_new_category_negative_untitled():
    """Test negative Add new category on database"""

    data = {"color": "blue"}

    with pytest.raises(ValueError):
        add_new_category(data)


@pytest.mark.unit
def test_add_new_category_negative_without_color():
    """Test negative Add new category on database"""

    data = {"title": "Humor"}

    with pytest.raises(ValueError):
        add_new_category(data)


@pytest.mark.unit
def test_add_new_category_negative_category_exists():
    """Test negative Add new category on database"""

    data = {"title": "Humor", "color": "blue"}

    add_new_category(data)

    with pytest.raises(ValueError):
        add_new_category(data)


@pytest.mark.unit
def test_add_new_category_negative_title_empty():
    """Test negative Add new category on database"""

    data = {"title": " ", "color": "blue"}

    with pytest.raises(ValueError):
        add_new_category(data)


@pytest.mark.unit
def test_add_new_category_negative_color_empty():
    """Test negative Add new category on database"""

    data = {"title": "Humor", "color": "  "}

    with pytest.raises(ValueError):
        add_new_category(data)


@pytest.mark.unit
def test_delete_category_positive():
    """test delete one category by id"""

    data = {"title": "Humor", "color": "blue"}

    insert_data = add_new_category(data)

    assert insert_data == 1
    id = 1
    result = delete_category(id)

    assert result == f"Category {id} deleted"


@pytest.mark.unit
def test_delete_category_negative():
    """test delete one category by id"""

    id = 1
    with pytest.raises(FileNotFoundError):
        delete_category(id)


@pytest.mark.unit
def test_update_category_positive():
    """test update category info on database"""

    data = {"title": "Humor", "color": "blue"}

    add_new_category(data)

    new_data = {"title": "Comédia"}

    update_data = update_category(1, new_data)

    assert update_data == 1
    assert get_category_by_id(1)["title"] == "Comédia"


@pytest.mark.unit
def test_update_category_positive_without_title():
    """test update category info on database"""

    data = {"title": "Humor", "color": "blue"}
    insert_data = add_new_category(data)
    assert insert_data == 1

    new_data = {"color": "red"}

    update_data = update_category(1, new_data)

    assert update_data == 1
    assert get_category_by_id(1)["color"] == "red"


@pytest.mark.unit
def test_update_category_negative():
    """test update category info on database"""

    data = {"title": "Humor", "color": "blue"}
    insert_data = add_new_category(data)

    assert insert_data == 1

    new_data = {"title": "Novos Rumos"}

    with pytest.raises(FileNotFoundError):
        update_category(2, new_data)


@pytest.mark.unit
def test_get_all_videos_by_category():
    """Test get all videos by category from database and list information"""

    data = {"title": "Humor", "color": "blue"}

    insert_data = add_new_category(data)
    assert insert_data == 1

    data_video = convert_json_for_dict(VIDEO_FILE)
    insert_data_video = add_new_video(data_video)

    assert insert_data_video == 1

    result = get_all_videos_by_category(1)

    assert result["1"]["title"] == "Git e Github para iniciantes"


@pytest.mark.unit
def test_get_all_videos_by_category_negative():
    """Test get all videos by category from database and list information"""

    data = {"title": "Humor", "color": "blue"}

    insert_data = add_new_category(data)
    assert insert_data == 1

    data_video = convert_json_for_dict(VIDEO_FILE)
    insert_data_video = add_new_video(data_video)

    assert insert_data_video == 1

    with pytest.raises(FileNotFoundError):
        get_all_videos_by_category(2)
