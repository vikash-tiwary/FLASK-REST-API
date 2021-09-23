import requests
import json

    
def test_create_user():
    """
    Test create user function
    """
    data={
        "name":"user title",
        "password":"12345"
    }

    response = requests.post("http://127.0.0.1:5000/user/post", json=json.dumps(data))

    assert 401== response.status_code


def test_get_all_users():
    """
    Test case to get all data from User details
    """
    response=requests.get("http://127.0.0.1:5000/user/get")

    assert 401==response.status_code


def test_get_one_user():
    """
    Test case to get one user from User details
    """
    response=requests.get("http://127.0.0.1:5000/user/get/c15cbf3c-050f-470b-af77-f5048fd86f54")

    assert 401==response.status_code

def test_promote_user():
    """
    Test case to update User details
    """
    data={
        "admin":"true"
    }
    response=requests.put("http://127.0.0.1:5000/user/update/c15cbf3c-050f-470b-af77-f5048fd86f54",json=json.dumps(data))

    assert 401==response.status_code


def test_delete_user():
    """
    Test case to delete user
    """
    response=requests.delete("http://127.0.0.1:5000/user/delete/c15cbf3c-050f-470b-af77-f5048fd86f54")

    assert 401==response.status_code
