import pytest
from django.urls import reverse
from shop.models import ShoppingCart, ShoppingCartProduct, Product, Address, Category, Tool


@pytest.mark.django_db
def test_checkout_view_get(client, user, cart, address):
    client.force_login(user)

    # Add an address for the user
    Address.objects.create(user=user, name='Test Address', street='123 Test Street', city='Test City', zipcode='12345')

    response = client.get(reverse('checkout'))

    assert response.status_code == 200
    assert 'shop/checkout.html' in [t.name for t in response.templates]
    assert 'Test Address' in response.content.decode()


@pytest.mark.django_db
def test_checkout_view_post(client, user, cart, address, test_product):
    client.force_login(user)
    ShoppingCartProduct.objects.create(shopping_cart=cart, product=test_product, quantity=2)

    # Add another product to the cart
    another_product = Product.objects.create(
        name='Another Product',
        netto_price=200,
        vat='0.11',
        category=test_product.category
    )
    ShoppingCartProduct.objects.create(shopping_cart=cart, product=another_product, quantity=1)

    # Perform POST request with address_id
    response = client.post(reverse('checkout'), {'address_id': address.id})

    # Calculate expected total
    total = 2 * (100 + (100 * 0.24)) + 200 + (200 * 0.11)

    assert response.status_code == 200
    assert 'shop/checkout.html' in [t.name for t in response.templates]
    assert f'{total}' in response.content.decode()
    assert 'Test City' in response.content.decode()
    assert '123 Test Street' in response.content.decode()
    assert '12345' in response.content.decode()



@pytest.mark.django_db
def test_checkout_view_no_active_cart(client, user):
    client.force_login(user)

    # Ensure the user has no active cart
    ShoppingCart.objects.filter(user=user).update(active=False)

    response = client.get(reverse('checkout'))

    # Since there is no active cart, it should return a 404 error
    assert response.status_code == 404
