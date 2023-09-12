import pytest
from click.testing import CliRunner

from api.commands import (
    delete,
    delete_category_by_id,
    new_category,
    new_video,
    search,
    show,
    show_category,
    show_one,
    show_one_category,
    show_videos_by_category,
    update,
    update_category_by_id,
)
from api.controller import add_new_category, add_new_video
from api.plugins import convert_json_for_dict
from tests.constants import (
    CATEGORY_FILE,
    CATEGORY_FILE_2,
    VIDEO_FILE,
    VIDEO_FILE_UPDATE_3,
)

cmd = CliRunner()


@pytest.mark.integration
def test_show_positive():
    """Test list all videos in CLI"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    out = cmd.invoke(show)

    assert out.exit_code == 0
    assert "Git e Github para iniciantes" in out.output


@pytest.mark.integration
def test_show_one_positive():
    """Test list one video by id in CLI"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    out = cmd.invoke(show_one, "1")

    assert out.exit_code == 0
    assert "Git e Github para iniciantes" in out.output


@pytest.mark.integration
def test_new_video_positive():
    """Test Add new video on database in CLI"""

    out = cmd.invoke(new_video, VIDEO_FILE)

    assert out.exit_code == 0
    assert "1" in out.output
    assert "Git e Github para iniciantes" in out.output


@pytest.mark.integration
def test_delete_positive():
    """Test Delete one video by id in CLI"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    out = cmd.invoke(delete, "1")

    assert out.exit_code == 0
    assert "Video deleted" in out.output


@pytest.mark.integration
def test_update_positive():
    """Test Update video infor on database in CLI"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    out = cmd.invoke(update, ["1", VIDEO_FILE_UPDATE_3])

    assert out.exit_code == 0
    assert "Introdução à programação em Go" in out.output


@pytest.mark.integration
@pytest.mark.parametrize("word", ["iniciantes", "github"])
def test_search_positive(word):
    """Test List all videos match with search in CLI"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    out = cmd.invoke(search, [word])

    assert out.exit_code == 0
    assert "Git e Github para iniciantes" in out.output


@pytest.mark.integration
def test_show_category_positive():
    """Test List all category in CLI"""

    data = {"title": "Humor", "color": "blue"}
    add_new_category(data)

    out = cmd.invoke(show_category)

    assert out.exit_code == 0
    assert "Humor" in out.output


@pytest.mark.integration
def test_show_one_category_positive():
    """Test List only one category by id in CLI"""

    data = {"title": "Humor", "color": "blue"}
    add_new_category(data)

    out = cmd.invoke(show_one_category, ["1"])

    assert out.exit_code == 0
    assert "Humor" in out.output


@pytest.mark.integration
def test_new_category_positive():
    """Test Add new category on database id in CLI"""

    out = cmd.invoke(new_category, [CATEGORY_FILE])

    assert out.exit_code == 0
    assert "Humor" in out.output


@pytest.mark.integration
def test_delete_category_by_id_positive():
    """Test Delete one category by id in CLI"""

    data = {"title": "Humor", "color": "blue"}
    add_new_category(data)

    out = cmd.invoke(delete_category_by_id, ["1"])

    assert out.exit_code == 0
    assert "Category 1 deleted" in out.output


@pytest.mark.integration
def test_update_category_by_id_positive():
    """Test Update category infor on database id in CLI"""

    data = {"title": "Humor", "color": "blue"}
    add_new_category(data)

    out = cmd.invoke(update_category_by_id, ["1", CATEGORY_FILE_2])

    assert out.exit_code == 0
    assert "Terror" in out.output


@pytest.mark.integration
def test_show_videos_by_category_positive():
    """Test List all videos by category in CLI"""

    add_new_video(convert_json_for_dict(VIDEO_FILE))

    data = {"title": "Humor", "color": "blue"}
    add_new_category(data)

    out = cmd.invoke(show_videos_by_category, ["1"])

    assert out.exit_code == 0
    assert "Git e Github para iniciantes" in out.output
