from flask import Flask
from flask_jwt_extended import create_access_token
from flask_simplelogin import SimpleLogin
from werkzeug.security import check_password_hash, generate_password_hash

from api.database import mongo


def create_token(username: str) -> str:
    """Creates tokens for user"""
    token = create_access_token(identity=username, expires_delta=False)

    return token


def create_user(**data) -> dict:
    """Creates user with encrypted password"""
    if "username" not in data or "password" not in data:
        raise ValueError("username and password are required.")

    data["password"] = generate_password_hash(
        data.pop("password"), method="pbkdf2:sha256"
    )

    data["token"] = create_token(data["username"])

    mongo.db.users.insert_one(data)
    return data


def validate_login(data):
    """Check that incoming credentials matches database stored credentials."""
    if "username" not in data or "password" not in data:
        raise ValueError("username and password are required.")

    db_user = mongo.db.users.find_one({"username": data["username"]})
    if db_user and check_password_hash(db_user["password"], data["password"]):
        return True

    return False


def configure(app: Flask):
    SimpleLogin(app, login_checker=validate_login)
