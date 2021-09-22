import requests
import json


def test_add_post():
    """
    Test function to create post details
    """
    data={
        "title":'title',
        "description":'description'
    }

    response = requests.post("http://127.0.0.1:5000/post/post",json=json.dumps(data))
    assert 401==response.status_code


def test_get_post():
    """
    Test function to get all post from post
    """
    response = requests.get("http://127.0.0.1:5000/post/get")
    assert 401==response.status_code

def test_post_details():
    """
    Test function to get post of one id from  post
    """
    response = requests.get("http://127.0.0.1:5000/post/post_details/1")
    assert 401==response.status_code

def test_post_update():
    """
    Test case to update pust details
    """
    data={ 
        "title":"title2",
        "description":"description2"
        
    }
    response=requests.put("http://127.0.0.1:5000/post/post_update/1",json=json.dumps(data))

    assert 401==response.status_code

def test_post_delete():
    """
    Test case to delete post
    """
    response=requests.delete("http://127.0.0.1:5000/post/delete/2")

    assert 401==response.status_code

