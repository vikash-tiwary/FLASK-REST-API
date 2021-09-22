from api.models.post_models import Post,Author,Address
import requests
import json


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
