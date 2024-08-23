import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_view(client, test_category):
    response = client.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view_uses_correct_template(client):
    response = client.get(reverse('index'))
    assert 'shop/base.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_index_view_context(client, test_category):
    response = client.get(reverse('index'))
    assert 'categories' in response.context
    assert len(response.context['categories']) == 1
    assert response.context['categories'][0].name == "Test Category"
