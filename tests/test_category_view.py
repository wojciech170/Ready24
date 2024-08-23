import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_category_view(client, test_category):
    response = client.get(reverse('categories', kwargs={'slug': test_category.slug}))
    assert response.status_code == 200
    assert test_category.name in response.content.decode()

@pytest.mark.django_db
def test_category_filter_view(client, test_category, test_product, test_tools):
    response = client.get(reverse('categories', kwargs={'slug': test_category.slug}))
    for tool in  test_product.tool.all():
        assert tool.name in response.content.decode()

@pytest.mark.django_db
def test_category_view_404(client):
    response = client.get(reverse('categories', args=["non-existent-category"]))
    assert response.status_code == 404
