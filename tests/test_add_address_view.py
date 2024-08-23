import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from shop.models import Address


@pytest.mark.django_db
def test_add_address_view_get_authenticated(client, user):
    client.force_login(user)
    response = client.get(reverse('add_address'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.wsgi_request.path == reverse('add_address')
    assertTemplateUsed(response, 'shop/add_address.html')

@pytest.mark.django_db
def test_add_address_view_get_unauthenticated(client):
    response = client.get(reverse('add_address'))
    assert response.status_code == 302
    assert response.url == '/login/?next=/profile/addaddress/'


@pytest.mark.django_db
def test_add_address_view_post_valid_form(client, user):
    client.force_login(user)
    form_data = {
        'name': 'Test Address',
        'city': 'Test City',
        'zipcode': '12345',
        'street': 'Test Street',
    }
    response = client.post(reverse('add_address'), data=form_data)

    assert response.status_code == 302
    assert response.url == reverse('profile', kwargs={'username': user.username})

    address = Address.objects.filter(user=user, name='Test Address').first()
    assert address is not None
    assert address.city == 'Test City'
    assert address.zipcode == '12345'
    assert address.street == 'Test Street'


@pytest.mark.django_db
def test_add_address_view_post_invalid_form(client, user):
    client.force_login(user)
    form_data = {
        'name': '',
        'city': 'Test City',
        'zipcode': '12345',
        'street': 'Test Street',
    }
    response = client.post(reverse('add_address'), data=form_data)

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert response.wsgi_request.path == reverse('add_address')
    assertTemplateUsed(response, 'shop/add_address.html')
    assert not Address.objects.filter(user=user, city='Test City').exists()
