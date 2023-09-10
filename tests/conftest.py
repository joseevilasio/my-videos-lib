import pytest

from api.app import create_app
from api.database import mongo

MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""


@pytest.fixture(scope="module")
def app():
    """Instace of Main flask app"""
    return create_app()


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


@pytest.fixture(autouse=True)
def setup_testing_database():
    """For each test, create a database."""

    app = create_app()
    mongo.init_app(app, uri="mongodb://localhost:27017/database_test")

    yield mongo
    mongo.cx.drop_database("database_test")
