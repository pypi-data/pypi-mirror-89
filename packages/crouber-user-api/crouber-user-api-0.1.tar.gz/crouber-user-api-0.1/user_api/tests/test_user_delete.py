from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


@pytest.fixture
def client():
    '''Return APIClient'''
    return APIClient()


@pytest.fixture
def login_url():
    '''Return a url path to user detail'''
    return reverse('login')


@pytest.fixture
def me_url():
    '''Return a url path to user detail'''
    return reverse('customuser-me')


@pytest.fixture
def list_url():
    '''Return a url path to user detail'''
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


def test_delete_user_if_logged_in(create_user, login_url, me_url, client):
    user = create_user
    instance = User.objects.get(email=user.data['email'])

    assert instance.email == user.data['email']

    data = {"current_password": "secretedss"}
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    login = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        login.data['auth_token']))
    resp = client.delete(me_url, data=data)

    assert resp.status_code == status.HTTP_204_NO_CONTENT

    try:
        instance = User.objects.get(email=user.data['email'])
    except ObjectDoesNotExist:
        instance = None

    assert instance is None


def test_delete_fail_password_validation(create_user, login_url, me_url,
                                         client):
    user = create_user
    instance = User.objects.get(email=user.data['email'])

    assert instance.email == user.data['email']

    data = {"current_password": "secreted"}
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    login = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        login.data['auth_token']))
    resp = client.delete(me_url, data=data)
    print(resp)
    print(resp.data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {"current_password": ["Invalid password."]}


def test_logged_user_cannot_delete_other_user(create_user, login_url,
                                              client):
    '''Test that authenticated user cannot delete
    other user instances'''
    create_user
    user2 = User.objects.create_user(
        firstname="jons",
        lastname="saint-patrick",
        email="jonst@gmail.com",
        password="secretedsqw",
    )
    data = {"current_password": "secretedsqw"}
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    auth = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        auth.data['auth_token']))
    resp = client.delete(
        reverse('customuser-detail', args={user2.pk}),
        data=data,
        format='json')

    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_cannot_delete_other_user(create_user, login_url,
                                  client):
    '''Test that non-authenticated users cannot delete
    other user instances'''
    user2 = User.objects.create_user(
        firstname="jons",
        lastname="saint-patrick",
        email="jonst@gmail.com",
        password="secretedsqw",
    )
    data = {"current_password": "secretedsqw"}
    resp = client.delete(
        reverse('customuser-detail', args={user2.pk}),
        data=data,
        format='json')

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_superuser_can_delete_users():
    '''Test that super user can delete other users'''
    pass
