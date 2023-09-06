from __future__ import annotations

import pymongo
import pytest
from dynaconf import settings

from tests.src import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    return app


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


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


@pytest.fixture(autouse=True, scope="module")
def setup_testing_database():
    """For each test, create a database."""
    test_client = pymongo.MongoClient("mongodb://localhost:27017/")
    database_test = test_client["database_test"]
    yield database_test
    test_client.drop_database("database_test")
