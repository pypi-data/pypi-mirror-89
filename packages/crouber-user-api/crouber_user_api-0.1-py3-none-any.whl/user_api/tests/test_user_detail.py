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


@pytest.fixture
def pk_url(create_user):
    '''Return a url path to user detail'''
    resp = create_user
    url = reverse('customuser-detail', None, {resp.data['id']})
    return url


@pytest.fixture
def login_url():
    '''Return a url path to user detail'''
    return reverse('login')


def test_unauthenticated_user_cannot_detail_user(client, pk_url):
    '''Test unauthenticated user's access to users endponts'''
    resp = client.get(pk_url, format='json')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_get_own_detail(client, pk_url, login_url):
    '''Test authenticated user can view their details'''
    url = pk_url
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    auth = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        auth.data['auth_token']))

    resp = client.get(url, format='json')

    assert resp.status_code == status.HTTP_200_OK


def test_user_cannot_get_other_user_detail(create_user, client, pk_url,
                                           login_url):
    '''Test authenticated user cannot access
    other user details
    '''
    user2 = User.objects.create_user(
        firstname="jons",
        lastname="saint-patrick",
        email="jonst@gmail.com",
        password="secretedss",
    )
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    auth = client.post(login_url, login_data, format='json')
    print(auth)
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        auth.data['auth_token']))
    resp = client.get(reverse("customuser-detail", args={user2.pk}))

    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_patch_own_user_details(client, pk_url, login_url):
    '''Test that user can edit its attributes'''
    url = pk_url
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    user = User.objects.get(email=login_data["email"])

    assert user.profile.state is None

    auth = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        auth.data['auth_token']))
    new_data = {
        "lastname": "GHOST",
        "profile": {
            "state": "TX"
        },
    }
    resp = client.patch(url, new_data, format='json')

    assert resp.status_code == status.HTTP_200_OK
    assert user.lastname != resp.data['lastname']
    assert user.profile.state != resp.data['profile']['state']


def test_cannot_patch_other_user_details(create_user, client, login_url):
    '''Test that authenticated user cannot edit
    other users'''
    user2 = User.objects.create_user(
        firstname="jons",
        lastname="saint-patrick",
        email="jonst@gmail.com",
        password="secretedss",
    )
    create_user
    login_data = {"email": "justinst@gmail.com",
                  "password": "secretedss", }
    auth = client.post(login_url, login_data, format='json')
    client.credentials(HTTP_AUTHORIZATION="Token {0}".format(
        auth.data['auth_token']))
    new_data = {
        "lastname": "GHOST",
        "profile": {
            "state": "TX"
        },
    }
    resp = client.patch(
        reverse("customuser-detail", args={user2.pk}),
        new_data,
        format='json')

    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_superuser_can_get_other_user_detail():
    '''Test that admin user can access other user's detail'''
    pass


def test_superuser_put_other_users():
    '''Test that admin user can update other users'''
