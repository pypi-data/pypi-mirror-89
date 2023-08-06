from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    '''Return APIClient'''
    return APIClient()


@pytest.fixture
def me_url():
    '''Return a url path to user detail'''
    return reverse('customuser-me')


@pytest.fixture
def login_url(db):
    '''Return a url path to user detail'''
    return reverse('login')


@pytest.fixture
def list_url():
    '''Return a url path to user list'''
    return reverse('customuser-list')


@pytest.fixture
def user_data(db):
    '''Return user input for creating new users'''
    data = {
        "firstname": "james",
        "lastname": "saint-patrick",
        "email": "justinst@gmail.com",
        "password": "secretedss",
    }
    return data


@pytest.fixture
def create_user(db, list_url, user_data, client):
    '''Create a test user'''
    resp = client.post(list_url, user_data, format='json')
    return resp


def test_return_user(create_user, login_url, me_url, client):
    '''Test return user detail @ me_url'''
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    login = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        login.data['auth_token']))
    resp = client.get(me_url, format='json')

    assert resp.status_code == status.HTTP_200_OK


def test_put_email_no_activation_email(create_user, login_url, me_url, client):
    '''Test that user can change email attribute'''
    pass
