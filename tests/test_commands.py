import pytest
from click.testing import CliRunner

from api.commands import (
    show,
    show_one,
    new_video,
)

from api.controller import add_new_video
from api.plugins import convert_json_for_dict
from tests.constants import VIDEO_FILE

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
def new_video_positive():
    """Test Add new video on database in CLI"""  

    out = cmd.invoke(new_video, VIDEO_FILE)

    assert out.exit_code == 0
    assert "1" in out.output
    assert "Git e Github para iniciantes" in out.output
