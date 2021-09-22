import requests
import json

def test_login():
    """
    Test the function getting auth token
    """
    data={
        "name":"Admin",
        "password":"123"
    }

    response=requests.get("http://127.0.0.1:5000/user/login")

    assert 401==response.status_code

