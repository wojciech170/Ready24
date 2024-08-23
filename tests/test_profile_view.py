import pytest
from django.urls import reverse
from shop.models import Address


@pytest.mark.django_db
def test_profile_view_status_code(client, user):
    client.login(username='test_user', password='test_password')
    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view_template(client, user):
    client.login(username='test_user', password='test_password')
    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)
    assert 'shop/profile_view.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_profile_view_context(client, user):
    client.login(username='test_user', password='test_password')
    Address.objects.create(user=user, street='123 Test St', city='San Francisco', zipcode='123456')
    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)
    assert 'user' in response.context
    assert response.context['user'] == user
    assert 'addresses' in response.context
    assert response.context['addresses'].count() == 1


@pytest.mark.django_db
def test_profile_view_redirects_if_not_authenticated(client, user):
    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login') + '?next=')
    assert response.url == f"{reverse('login')}?next={url}"
