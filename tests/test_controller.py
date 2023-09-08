import pytest

from api.controller import (
    add_new_video,
    delete_video,
    get_all_videos,
    get_video_by_id,
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
def test_delete_video_positive():
    """test delete one video by id"""

    data = convert_json_for_dict(VIDEO_FILE)
    insert_data = add_new_video(data)

    assert insert_data == 1
    id = 1
    result = delete_video(id)

    assert result == f"Video {id} deleted"
