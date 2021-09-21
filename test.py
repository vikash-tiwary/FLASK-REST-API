from api.models import User,Post,Author,Address
import requests
import json

def test_user():
    """
    Test the user model
    """
    user=User(name="mohan",password="12345")
    assert user.name=="mohan"
    assert user.password=="12345"


def test_post():
    """
    Test the Post model
    """
    post=Post(title="title",description="description")
    assert post.title=="title"
    assert post.description=="description"


def test_author():
    """
    Test the Author model
    """
    author=Author(name="vickey",post_id="1")
    assert author.name=="vickey"
    assert author.post_id=="1"

def test_address():
    """
    Test the Address model
    """
    address=Address(details="Gujrat",author_id="1")
    assert address.details=="Gujrat"
    assert address.author_id=="1"

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

    
def test_create_user():
    """
    Test create user function
    """
    data={
        "name":"user title",
        "password":"12345"
    }

    response = requests.post("http://127.0.0.1:5000/user/user", json=json.dumps(data))

    assert 401== response.status_code


def test_get_all_users():
    """
    Test case to get all data from User details
    """
    response=requests.get("http://127.0.0.1:5000/user/user")

    assert 401==response.status_code


def test_get_one_user():
    """
    Test case to get one user from User details
    """
    response=requests.get("http://127.0.0.1:5000/user/user/c15cbf3c-050f-470b-af77-f5048fd86f54")

    assert 401==response.status_code

def test_promote_user():
    """
    Test case to update User details
    """
    data={
        "admin":"true"
    }
    response=requests.put("http://127.0.0.1:5000/user/user/c15cbf3c-050f-470b-af77-f5048fd86f54",json=json.dumps(data))

    assert 401==response.status_code


def test_delete_user():
    """
    Test case to delete user
    """
    response=requests.delete("http://127.0.0.1:5000/user/user/c15cbf3c-050f-470b-af77-f5048fd86f54")

    assert 401==response.status_code


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


def test_add_author():
    """
    Test function to create author details
    """
    data={
        "name":'raj',
        "post_id":'1'
    }

    response = requests.post("http://127.0.0.1:5000/post/author/1",json=json.dumps(data))
    assert 401==response.status_code


def test_get_author():
    """
    Test function to get all author from author
    """
    response = requests.get("http://127.0.0.1:5000/post/get_author")
    assert 401==response.status_code

def test_get_author_id():
    """
    Test function to get author of one id from author
    """
    response = requests.get("http://127.0.0.1:5000/post/get_author/1")
    assert 401==response.status_code

def test_author_update():
    """
    Test case to update author details
    """
    data={ 
        "name":"tilu"
    }
    response=requests.put("http://127.0.0.1:5000/post/author_update/1",json=json.dumps(data))

    assert 401==response.status_code

def test_author_delete():
    """
    Test case to delete author
    """
    response=requests.delete("http://127.0.0.1:5000/post/author_delete/2")

    assert 401==response.status_code


def test_add_address():
    """
    Test function to create address details
    """
    data={
        "details":'Haldia',
        "author_id":'1'
    }

    response = requests.post("http://127.0.0.1:5000/post/address/1",json=json.dumps(data))
    assert 401==response.status_code


def test_get_address():
    """
    Test function to get all address details
    """
    response = requests.get("http://127.0.0.1:5000/post/get_address")
    assert 401==response.status_code

def test_get_address_id():
    """
    Test function to get post of one id from  address
    """
    response = requests.get("http://127.0.0.1:5000/post/get_address/1")
    assert 401==response.status_code

def test_address_update():
    """
    Test case to update address
    """
    data={ 
        "details":"Haldia doc"
    }
    response=requests.put("http://127.0.0.1:5000/post/address_update/1",json=json.dumps(data))

    assert 401==response.status_code

def test_address_delete():
    """
    Test case to delete Address
    """
    response=requests.delete("http://127.0.0.1:5000/post/address_delete/2")

    assert 401==response.status_code