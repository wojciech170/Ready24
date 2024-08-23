import pytest
from django.urls import reverse
from shop.forms import LoginForm


@pytest.mark.django_db
def test_products_view(client, test_product):
    response = client.get(reverse('product', kwargs={'slug': test_product.slug}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_products_view_404(client):
    response = client.get(reverse('product', args=["non-existent-product"]))
    assert response.status_code == 404
