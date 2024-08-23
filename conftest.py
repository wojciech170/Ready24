import pytest

from django.test import Client
from django.contrib.auth.models import User
from shop.models import Product, Tool, Category

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
    )
    test_product.tool.set([test_tool])
    return test_product

@pytest.fixture
def user():
    return User.objects.create_user(username='test_user', password='test_password')