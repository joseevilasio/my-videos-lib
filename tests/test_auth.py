import pytest

from api.auth import create_user, validate_login
from api.database import mongo


@pytest.mark.integration
def test_create_user_positive():
    """Test creates user with encrypted password"""

    create_user(username="admin", password="123456")

    username = mongo.db.users.find_one(
        {"username": "admin"}, projection={"_id": False}
    )["username"]

    assert "admin" == username


@pytest.mark.integration
def test_create_user_negative_without_username():
    """Test negative creates user with encrypted password"""

    with pytest.raises(ValueError):
        create_user(password="123456")


@pytest.mark.integration
def test_create_user_negative_without_password():
    """Test negative creates user with encrypted password"""

    with pytest.raises(ValueError):
        create_user(username="admin")


@pytest.mark.integration
def test_validate_login_negative_without_username():
    """Test negative Check that incoming credentials matches
    database stored credentials."""

    data = {"password": "123456"}

    with pytest.raises(ValueError):
        validate_login(data)


@pytest.mark.integration
def test_validate_login_negative_without_password():
    """Test negative Check that incoming credentials matches
    database stored credentials."""

    data = {"username": "admin"}

    with pytest.raises(ValueError):
        validate_login(data)


@pytest.mark.integration
def test_validate_login_positive():
    """Test Check that incoming credentials matches
    database stored credentials."""

    data = {"username": "admin", "password": "123456"}

    create_user(**data)
    result = validate_login(data)

    assert result is True


@pytest.mark.integration
def test_validate_login_negative_wrong_password():
    """Test Check that incoming credentials matches
    database stored credentials."""

    data = {"username": "admin", "password": "123456"}
    data_wrong = {"username": "admin", "password": "456123"}

    create_user(**data)
    result = validate_login(data_wrong)

    assert result is False
