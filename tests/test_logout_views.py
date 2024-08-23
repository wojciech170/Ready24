import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username='test_user', password='test_password')
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302