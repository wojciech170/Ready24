import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from shop.forms import UserForm


@pytest.mark.django_db
def test_create_user_view_get(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200
    assert isinstance(response.context['form'], UserForm)


@pytest.mark.django_db
def test_create_user_view_post_valid(client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'password1': 'newpassword',
        'password2': 'newpassword',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_create_user_view_post_invalid(client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'password1': 'newpassword',
        'password2': 'wrongpassword',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context