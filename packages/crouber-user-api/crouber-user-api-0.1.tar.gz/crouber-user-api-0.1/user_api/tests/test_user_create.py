from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model
from . utils_ts import assert_instance_exist

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
def detail_url():
    '''Return a url path to user detail'''
    return reverse('customuser-me')


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


def test_post_create_user_without_login(create_user, user_data):
    '''Test that we can create a user, the response does not
    contain any password and the password passes its checks
    '''
    response = create_user
    data = user_data
    user = User.objects.get(email=data["email"])

    assert response.status_code == status.HTTP_201_CREATED
    assert ("password" not in response.data)
    assert (user.check_password(data["password"]))
    assert (assert_instance_exist(User, data["email"]))


def test_post_email_exists(create_user, client, list_url, user_data):
    response1 = create_user

    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post(list_url, user_data, format='json')

    assert response2.status_code == status.HTTP_400_BAD_REQUEST


def test_post_not_register_if_fails_password_validation(db, client, list_url):
    data = {
        "firstname": "james",
        "lastname": "saint-patrick",
        "email": "justinst@gmail.com",
        "password": "666",
    }
    response = client.post(list_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_post_return_400_for_integrity_error(db, client, list_url):
    data = {
        "firstname": "james",
        "lastname": "saint-patrick",
        "email": "justinst@gmail.com",
        "password": "secret",
    }
    response = client.post(list_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_post_missing_required_fields(db, client, list_url):
    data = {
        "lastname": "saint-patrick",
        "email": "justinst@gmail.com",
        "password": "secret",
    }
    response = client.post(list_url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["firstname"][0].code == "required"


def test_post_not_register_if_password_mismatch(db, client, list_url):
    pass


def test_post_create_user_with_login_and_send_activation_email():
    pass


def test_user_create_with_retype_password():
    pass
