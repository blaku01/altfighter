import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient


@pytest.fixture
def client_group():
    return Group.objects.create(name="client")


@pytest.fixture
def client_user(client_group):
    user_model = get_user_model()
    client_login = "client_user"
    client_password = "client_password"
    user = user_model.objects.create_user(username=client_login, password=client_password)
    user.groups.add(client_group)
    user.save()
    return {"user": user, "username": client_login, "password": client_password}


@pytest.fixture
def seller_group():
    return Group.objects.create(name="seller")


@pytest.fixture
def seller_user(seller_group):
    user_model = get_user_model()
    seller_login = "seller_user"
    seller_password = "seller_password"
    user = user_model.objects.create_user(username=seller_login, password=seller_password)
    user.groups.add(seller_group)
    user.save()
    return {"user": user, "username": seller_login, "password": seller_password}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client_api_client(api_client, client_user):
    """API client for regular clients (users who are not sellers)."""
    return api_client.login(username=client_user["username"], password=client_user["password"])


@pytest.fixture
def seller_api_client(api_client, seller_user):
    """API client for sellers."""
    return api_client.login(username=seller_user["username"], password=seller_user["password"])
