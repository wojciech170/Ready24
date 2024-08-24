import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_search_view_get_request(client):
    response = client.get(reverse('search'))
    assert response.status_code == 200
    assert 'shop/search.html' in [t.name for t in response.templates]
    assert 'form' in response.context


@pytest.mark.django_db
def test_search_view_post_request_with_results(client, test_product):
    response = client.post(reverse('search'), {'searched': 'Test Product'})
    assert response.status_code == 200
    assert 'shop/search.html' in [t.name for t in response.templates]
    assert 'products' in response.context
    assert len(response.context['products']) == 1
    assert response.context['products'][0].name == "Test Product"


@pytest.mark.django_db
def test_search_view_post_request_no_results(client, test_product):
    response = client.post(reverse('search'), {'searched': 'Nonexistent Product'})
    assert response.status_code == 200
    assert 'shop/search.html' in [t.name for t in response.templates]
    assert 'products' in response.context
    assert len(response.context['products']) == 0


@pytest.mark.django_db
def test_search_view_post_request_invalid_form(client):
    response = client.post(reverse('search'), {'searched': ''})
    assert response.status_code == 200
    assert 'shop/search.html' in [t.name for t in response.templates]
    assert 'products' in response.context
    assert 'form' in response.context
    assert response.context['form'].errors
