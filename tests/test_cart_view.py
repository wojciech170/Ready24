import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import ShoppingCart, ShoppingCartProduct, Product, PromoCodes, Category



@pytest.mark.django_db
def test_cart_view_displays_cart(client, user, cart, cart_product):
    client.force_login(user)
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert 'shop/cart_view.html' in [t.name for t in response.templates]
    assert 'Test Product' in response.content.decode()
    assert '2' in response.content.decode()  # Quantity
    assert '248' in response.content.decode()  # Total price (2 * (100 + (100 * 0.24)))


@pytest.mark.django_db
def test_cart_view_no_cart_raises_404(client, user):
    client.force_login(user)

    response = client.get(reverse('cart'))
    assert response.status_code == 404


@pytest.mark.django_db
def test_cart_view_total_calculation(client, user, cart, test_product):
    client.force_login(user)
    ShoppingCartProduct.objects.create(shopping_cart=cart, product=test_product, quantity=3)
    another_product = Product.objects.create(
        name='Another Product',
        stock=5,
        netto_price=200,
        vat='0.11',
        category=test_product.category
    )
    ShoppingCartProduct.objects.create(shopping_cart=cart, product=another_product, quantity=1)

    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert 'Test Product' in response.content.decode()
    assert 'Another Product' in response.content.decode()
    assert '594' in response.content.decode()  # (3 * (100 + (100 * 0.24))) + (1 * (200 + (200 * 0.11)))


