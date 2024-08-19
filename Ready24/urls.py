"""
URL configuration for Ready24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop.views import (
    IndexView,
    CategoryView,
    LoginView,
    LogoutView,
    CreateUserView,
    ProductView,
    SearchView,
    ProfileView,
    AddAddressView,
    AddToCartView,
    CartView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('category/<slug>', CategoryView.as_view(), name='categories'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('product/<slug>', ProductView.as_view(), name='product'),
    path('search/', SearchView.as_view(), name='search'),
    path('profile/<username>', ProfileView.as_view(), name='profile'),
    path('profile/addaddress/', AddAddressView.as_view(), name='add_address'),
    path('profile/addtocart/', AddToCartView.as_view(), name='add_to_cart'),
    path('profile/<username>/cart/', CartView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)