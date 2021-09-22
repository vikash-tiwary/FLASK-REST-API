from api.models.users_models import User
import requests
import json

def test_user():
    """
    Test the user model
    """
    user=User(name="mohan",password="12345")
    assert user.name=="mohan"
    assert user.password=="12345"
