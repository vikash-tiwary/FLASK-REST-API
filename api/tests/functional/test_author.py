import requests
import json


def test_add_author():
    """
    Test function to create author details
    """
    data={
        "name":'raj',
        "post_id":'1'
    }

    response = requests.post("http://127.0.0.1:5000/author/post/1",json=json.dumps(data))
    assert 401==response.status_code


def test_get_author():
    """
    Test function to get all author from author
    """
    response = requests.get("http://127.0.0.1:5000/author/get")
    assert 401==response.status_code

def test_get_author_id():
    """
    Test function to get author of one id from author
    """
    response = requests.get("http://127.0.0.1:5000/author/get/1")
    assert 401==response.status_code

def test_author_update():
    """
    Test case to update author details
    """
    data={ 
        "name":"tilu"
    }
    response=requests.put("http://127.0.0.1:5000/author/update/1",json=json.dumps(data))

    assert 401==response.status_code

def test_author_delete():
    """
    Test case to delete author
    """
    response=requests.delete("http://127.0.0.1:5000/author/delete/2")

    assert 401==response.status_code

