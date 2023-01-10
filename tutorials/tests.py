from django.test import TestCase

from django.urls import reverse
import pytest
from tutorials.models import Tutorial
from django.urls import reverse
import pytest

# Create your tests here.

"""We will write a test to make sure that when we reverse the view named home, we get the expected path for the homepage on the website, which is "/". 
Add the following code to the tutorials/tests.py file:"""
def test_homepage_access():
    url = reverse('home')
    assert url == "/"
    
    
"""This test verifies that we are able to successfully create a Tutorial object in the database.
Run the test with the command pytest -k create. You will see this error:"""    


"""Notice how the test failed, but the reason is not that the tutorial could not be created.
The reason is that pytest does not have access to the database in order to run the test.
To fix this, we must again add the marker: @pytest.mark.django_db directly above the test function declaration:


Test access to the database is intentionally conservative, to ensure that database connection is always intended and not accidental. 
The decorator @pytest.mark.django_db is used to allow this test access to the connected database, which is required by this particular view. """ 

@pytest.mark.django_db
@pytest.fixture
def new_tutorial(db):
    tutorial = Tutorial.objects.create(
        title='Pytest',
        tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
        description='Tutorial on how to apply pytest to a Django application',
        published=True
    )
    return tutorial

"""These test functions use new_tutorial as a parameter. 
This causes the new_tutorial() fixture function to be run first when either of these tests is run.
The first test, test_search_tutorials(), simply checks that the object created by the fixture exists, by searching for an object with the same title.
The second test, test_update_tutorial, updates the title of the new_tutorial object, saves the update, and asserts that a tutorial with the updated name exists in the database. 
Inside this test function's body, new_tutorial refers not to the new_tutorial fixture function, but to the object returned from that fixture function."""


def test_search_tutorials(new_tutorial):
    assert Tutorial.objects.filter(title='Pytest').exists()

def test_update_tutorial(new_tutorial):
    new_tutorial.title = 'Pytest-Django'
    new_tutorial.save()
    assert Tutorial.objects.filter(title='Pytest-Django').exists()
    
"""These test functions use new_tutorial as a parameter. 
This causes the new_tutorial() fixture function to be run first when either of these tests is run.
The first test, test_search_tutorials(), simply checks that the object created by the fixture exists, 
by searching for an object with the same title.
The second test, test_update_tutorial, updates the title of the new_tutorial object, saves the update, 
and asserts that a tutorial with the updated name exists in the database. 
Inside this test function's body, new_tutorial refers not to the new_tutorial fixture function, 
but to the object returned from that fixture function."""    
    
def test_search_tutorials(new_tutorial):
    assert Tutorial.objects.filter(title='Pytest').exists()

def test_update_tutorial(new_tutorial):
    new_tutorial.title = 'Pytest-Django'
    new_tutorial.save()
    assert Tutorial.objects.filter(title='Pytest-Django').exists()   
    
    
"""Let's try one more integration test with fixtures, to show how multiple fixtures may be used in a test function.
To the tests.py file, add another fixture function that creates a different Tutorials object:"""


@pytest.fixture
def another_tutorial(db):
    tutorial = Tutorial.objects.create(
        title='More-Pytest',
        tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
        description='Tutorial on how to apply pytest to a Django application',
        published=True
    )
    return tutorial

"""Both the objects returned from the new_tutorial and another_tutorial fixtures are passed in.
Then, the test asserts that the .pk attributes are not equal to the other.
The .pk attribute in the Django ORM refers to the primary key of a database object, which is automatically generated when it is created.
Thus, this is simply asserting that the two objects are not the same as each other. """   


def test_compare_tutorials(new_tutorial, another_tutorial):
    assert new_tutorial.pk != another_tutorial.pk
    
""" fixture for creating a test user object in the database:"""  

@pytest.fixture
def test_user(db, django_user_model):
    django_user_model.objects.create_user(
        username="test_username", password="test_password")
    return "test_username", "test_password"   # this returns a tuple


"""This fixture creates a new user with the Django create_user() method and sets a username and password.
Then it returns the username and password as a tuple.  Let's write a function to test that logging into the app works, 
using the test_user fixture as a parameter to first add a user:"""

def test_login_user(client, test_user):
    test_username, test_password = test_user  # this unpacks the tuple
    login_result = client.login(username=test_username, password=test_password)
    assert login_result == True