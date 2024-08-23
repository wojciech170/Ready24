import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_view_status_code(client, test_product):
    url = reverse('product', kwargs={'slug': test_product.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_view_template(client, test_product):
    url = reverse('product', kwargs={'slug': test_product.slug})
    response = client.get(url)
    assert 'shop/product_view.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_product_view_context(client, test_product):
    url = reverse('product', kwargs={'slug': test_product.slug})
    response = client.get(url)
    assert 'product' in response.context
    assert response.context['product'] == test_product


@pytest.mark.django_db
def test_product_view_404_for_invalid_slug(client):
    invalid_slug = 'invalid-slug'
    url = reverse('product', kwargs={'slug': invalid_slug})
    response = client.get(url)
    assert response.status_code == 404
