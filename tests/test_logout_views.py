import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username='test_user', password='test_password')
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')


@pytest.mark.django_db
def test_logout_view_clears_session(client, user):
    client.login(username='test_user', password='test_password')
    url = reverse('logout')
    response = client.get(url)
    assert not client.session.get('_auth_user_id')


@pytest.mark.django_db
def test_logout_view_no_access_when_logged_out(client):
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')
