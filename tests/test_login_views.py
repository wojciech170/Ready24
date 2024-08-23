import pytest
from django.urls import reverse
from shop.forms import LoginForm


@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_login_view_post_valid(client, user):
    url = reverse('login')
    response = client.post(url, {'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_post_invalid(client):
    url = reverse('login')
    response = client.post(url, {'username': 'wrong_user', 'password': 'wrong_password'})
    assert response.status_code == 200
    assert 'form' in response.context
