from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model

from djoser.conf import settings

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


def test_post_should_login_user(create_user, client, login_url):
    '''Test user login'''
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    resp = client.post(login_url, login_data, format='json')
    user = User.objects.get(email=login_data["email"])

    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['auth_token'] == user.auth_token.key


def test_post_not_login_if_user_inactive(create_user, client, login_url):
    '''Test user login when user is inactive'''
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    user = User.objects.get(email=login_data["email"])
    user.is_active = False
    user.save()
    resp = client.post(login_url, login_data, format='json')
    expected_errors = [settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR]

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data["non_field_errors"] == expected_errors


def test_post_not_login_invalid_cred(create_user, client, login_url):
    create_user
    login_data = {"email": "jydgetsyu@gmail.com",
                  "password": "wronghusy", }
    resp = client.post(login_url, login_data, format='json')
    expected_errors = [settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR]

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data["non_field_errors"] == expected_errors


def test_post_not_login_if_empty_request(create_user, client, login_url):
    login_data = {}
    resp = client.post(login_url, login_data, format='json')
    expected_errors = [settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR]

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data["non_field_errors"] == expected_errors
