import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_view(client, test_category):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert test_category.name in response.content.decode()
