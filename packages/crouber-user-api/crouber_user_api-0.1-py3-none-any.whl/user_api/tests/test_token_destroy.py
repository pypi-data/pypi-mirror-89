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
    '''Return a url path to user detail'''
    return reverse('customuser-list')


@pytest.fixture
def login_url():
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


def test_post_should_logout_logged_in_user(create_user, client, login_url):
    '''Test logout user who is logged in'''
    data = create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    client.post(login_url, login_data, format='json')
    user = User.objects.get(email=data.data["email"])
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        user.auth_token.key))
    logout_url = reverse('logout')
    resp = client.post(logout_url)

    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert (resp.data) is None


def test_post_deny_logout_not_logged_in_user(create_user, client, login_url):
    '''Test logout user who is logged in'''
    create_user

    logout_url = reverse('logout')
    resp = client.post(logout_url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_options(create_user, client, login_url):
    '''Test logout options'''
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    resp = client.post(login_url, login_data, format='json')
    user = User.objects.get(email=login_data["email"])

    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        user.auth_token.key))
    logout_url = reverse('logout')

    resp = client.options(logout_url)

    assert resp.status_code == status.HTTP_200_OK
