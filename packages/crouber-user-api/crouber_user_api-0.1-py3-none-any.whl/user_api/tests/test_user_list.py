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
def list_url():
    '''Return a url path to user list'''
    return reverse('customuser-list')


@pytest.fixture
def login_url(db):
    '''Return a url path to user detail'''
    return reverse('login')


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


def test_unauthenticated_user_cannot_list_user(client, list_url):
    '''Test unauthenticated user's access to users endponts'''
    resp = client.get(list_url, format='json')

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_cannot_list_other_users(create_user, client, login_url, list_url): # noqa
    '''Test that authenticated user cannot view other users'''
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    login = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        login.data['auth_token']))
    resp = client.get(list_url, format='json')

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 1


def test_superuser_can_list_all_users():
    pass
