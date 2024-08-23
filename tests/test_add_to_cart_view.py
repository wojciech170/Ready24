import pytest
from django.shortcuts import redirect
from django.urls import reverse
from shop.models import ShoppingCart, ShoppingCartProduct, Product


@pytest.mark.django_db
def test_add_to_cart_creates_cart_if_not_exists(client, test_product, user):
    client.login(username='test_user', password='test_password')
    assert ShoppingCart.objects.filter(user=user, active=True).count() == 0
    response = client.post(reverse('add_to_cart'), {'product_id': test_product.id})
    assert response.status_code == 302
    assert ShoppingCart.objects.filter(user=user, active=True).count() == 1


@pytest.mark.django_db
def test_add_to_cart_creates_cart_product(client, test_product, user):
    client.login(username='test_user', password='test_password')

    response = client.post(reverse('add_to_cart'), {'product_id': test_product.id})
    assert response.status_code == 302
    cart = ShoppingCart.objects.get(user=user, active=True)
    cart_product = ShoppingCartProduct.objects.get(shopping_cart=cart, product=test_product)
    assert cart_product.quantity == 1


@pytest.mark.django_db
def test_add_to_cart_updates_existing_cart_product(client, test_product, user):
    client.login(username='test_user', password='test_password')

    cart = ShoppingCart.objects.create(user=user, active=True)
    cart_product = ShoppingCartProduct.objects.create(shopping_cart=cart, product=test_product, quantity=1)
    response = client.post(reverse('add_to_cart'), {'product_id': test_product.id})
    assert response.status_code == 302
    cart_product.refresh_from_db()
    assert cart_product.quantity == 2


@pytest.mark.django_db
def test_add_to_cart_redirects_after_addition(client, test_product, user):
    client.login(username='test_user', password='test_password')

    response = client.post(reverse('add_to_cart'), {'product_id': test_product.id, 'quantity': 1})
    assert response.status_code == 302
    assert response.url == reverse('cart')


@pytest.mark.django_db
def test_add_to_cart_invalid_product_id(client, user):
    client.login(username='test_user', password='test_password')

    response = client.post(reverse('add_to_cart'), {'product_id': 9999, 'quantity': 1})
    assert response.status_code == 404
