import pytest
from flask_jwt_extended import decode_token

from api.auth import create_token, create_user, validate_login
from api.plugins import jwt
from flask import Flask


@pytest.mark.unit
def test_positive_create_token():
    """Test positive ensure creates tokens for user"""
   
    username = "admin"
    result = create_token(username)

    assert decode_token(result).get("sub") == username


@pytest.mark.unit
def test_positive_create_user():
    """Test postive ensure creates user with encrypted password"""
    
    result = create_user(username="admin", password="123456")
    assert len(result) >= 1
