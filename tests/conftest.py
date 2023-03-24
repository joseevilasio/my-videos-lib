import pytest

from api.app import create_app


@pytest.fixture(scope="module")
def app():
    """Instace of Main flask app"""
    return create_app()
