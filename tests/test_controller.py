import pytest

from api.controller import (
    add_new_video,
    delete_video,
    get_all_videos,
    get_video_by_id,
    search_video,
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


@pytest.mark.unit
def test_get_all_videos_positive():
    """Test get all videos from database and list information"""

    data = convert_json_for_dict(VIDEO_FILE)

    assert get_all_videos() == {}

    insert_data = add_new_video(data)
    result = get_all_videos()

    assert insert_data == 1
    assert result["1"]["title"] == "Git e Github para iniciantes"


@pytest.mark.unit
@pytest.mark.parametrize("id", [1, 2])
def test_get_video_by_id_positive(id):
    """Test positive get video by id from database and list information"""

    data_1 = convert_json_for_dict(VIDEO_FILE)
    data_2 = convert_json_for_dict(VIDEO_FILE_2)
    add_new_video(data_1)
    add_new_video(data_2)

    result = get_video_by_id(id)

    assert result != FileExistsError


@pytest.mark.unit
@pytest.mark.parametrize("id", [3, 4])
def test_get_video_by_id_negative(id):
    """Test negative get video by id from database and list information"""

    data_1 = convert_json_for_dict(VIDEO_FILE)
    data_2 = convert_json_for_dict(VIDEO_FILE_2)
    add_new_video(data_1)
    add_new_video(data_2)

    with pytest.raises(FileExistsError):
        get_video_by_id(id)


@pytest.mark.unit
def test_add_new_video_positive():
    """Test positive Add new video on database"""

    data_1 = convert_json_for_dict(VIDEO_FILE)
    data_2 = convert_json_for_dict(VIDEO_FILE_2)
    result_1 = add_new_video(data_1)
    result_2 = add_new_video(data_2)

    assert result_1 == 1
    assert result_2 == 2


@pytest.mark.unit
def test_add_new_video_negative_untitled():
    """Test negative Add new video on database"""

    data = convert_json_for_dict(VIDEO_FILE_3_ERRO)

    with pytest.raises(FileExistsError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_without_description():
    """Test negative Add new video on database"""

    data = convert_json_for_dict(VIDEO_FILE_4_ERRO)

    with pytest.raises(FileExistsError):
        add_new_video(data)


@pytest.mark.unit
def test_add_new_video_negative_without_url():
    """Test negative Add new video on database"""

    data = convert_json_for_dict(VIDEO_FILE_5_ERRO)

    with pytest.raises(FileExistsError):
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

    with pytest.raises(FileExistsError):
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

    with pytest.raises(FileExistsError):
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

    data = convert_json_for_dict(VIDEO_FILE)
    insert_data = add_new_video(data)

    assert insert_data == 1
    id = 1
    result = delete_video(id)

    assert result == f"Video {id} deleted"


@pytest.mark.unit
def test_delete_video_negative():
    """test delete one video by id"""

    id = 1
    with pytest.raises(FileExistsError):
        delete_video(id)


@pytest.mark.unit
def test_search_video_positive():
    """test search video by string match"""

    data = convert_json_for_dict(VIDEO_FILE)
    insert_data = add_new_video(data)

    assert insert_data == 1

    word = "iniciante"
    result = search_video(word)
    print(result)


@pytest.mark.unit
def test_search_video_negative():
    """test search video by string match"""

    data = convert_json_for_dict(VIDEO_FILE)
    add_new_video(data)

    word = "tempo"

    with pytest.raises(FileExistsError):
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

    data = convert_json_for_dict(VIDEO_FILE)
    insert_data = add_new_video(data)

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

    data = convert_json_for_dict(VIDEO_FILE)
    insert_data = add_new_video(data)

    assert insert_data == 1

    new_data = {"title": "Novos Rumos"}

    with pytest.raises(FileExistsError):
        update_video(2, new_data)
