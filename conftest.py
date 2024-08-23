import pytest

from django.test import Client
from django.contrib.auth.models import User
from shop.models import Product, Tool, Category, ShoppingCart, ShoppingCartProduct, Address


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_tools():
    Tool.objects.create(name='Test Tool')
    Tool.objects.create(name='Test Tool 1')
    Tool.objects.create(name='Test Tool 2')


@pytest.fixture
def test_category():
    return Category.objects.create(name="Test Category", description="test category description")

@pytest.fixture
def test_product(test_category):
    test_tool = Tool.objects.create(name="Test Tool 3")
    test_product = Product.objects.create(
        name="Test Product",
        netto_price=100,
        category=test_category,
        vat='0.24'
    )
    test_product.tool.set([test_tool])
    return test_product

@pytest.fixture
def user():
    return User.objects.create_user(username='test_user', password='test_password')


@pytest.fixture
def cart(user):
    return ShoppingCart.objects.create(user=user, active=True)


@pytest.fixture
def cart_product(cart, test_product):
    return ShoppingCartProduct.objects.create(shopping_cart=cart, product=test_product, quantity=2)

@pytest.fixture
def address(user):
    return Address.objects.create(
        user=user,
        name="Test Address",
        street="123 Test Street",
        city="Test City",
        zipcode="12345"
    )