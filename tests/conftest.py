import warnings
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SAWarning
from sqlmodel import create_engine

from api import model
from api.app import create_app


@pytest.fixture(scope="module")
def app():
    """Instace of Main flask app"""
    return create_app()


warnings.filterwarnings("ignore", category=SAWarning)


MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield


@pytest.fixture(autouse=True, scope="function")
def setup_testing_database(request):
    """For each test, create a database file on tmpdir
    force database.py to use that filepath.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.db"))
    engine = create_engine(f"sqlite:///{test_db}")
    model.SQLModel.metadata.create_all(bind=engine)
    with patch("api.database.engine", engine):
        yield
