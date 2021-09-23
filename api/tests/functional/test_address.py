import requests
import json

def test_add_address():
    """
    Test function to create address details
    """
    data={
        "details":'Haldia',
        "author_id":'1'
    }

    response = requests.post("http://127.0.0.1:5000/address/post/1",json=json.dumps(data))
    assert 401==response.status_code


def test_get_address():
    """
    Test function to get all address details
    """
    response = requests.get("http://127.0.0.1:5000/address/get")
    assert 401==response.status_code

def test_get_address_id():
    """
    Test function to get post of one id from  address
    """
    response = requests.get("http://127.0.0.1:5000/author/get/1")
    assert 401==response.status_code

def test_address_update():
    """
    Test case to update address
    """
    data={ 
        "details":"Haldia doc"
    }
    response=requests.put("http://127.0.0.1:5000/address/update/1",json=json.dumps(data))

    assert 401==response.status_code

def test_address_delete():
    """
    Test case to delete Address
    """
    response=requests.delete("http://127.0.0.1:5000/address/delete/2")

    assert 401==response.status_code