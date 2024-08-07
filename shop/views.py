from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Product
from .forms import LoginForm, UserForm

from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()

categories = Category.objects.all()


class IndexView(View):
    def get(self, request):
        return render(request, "shop/base.html", {"categories": categories})


class CategoryView(View):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            products = Product.objects.filter(category=category)
            ctx = {
                "categories": categories,
                "category": category,
                "products": products
            }
            return render(request, "shop/category.html", ctx)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")


class ProductView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        ctx = {
            "product": product,
            "categories": categories,
        }
        return render(request, "shop/product.html", ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'shop/login.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user:
                login(request, user)
                return redirect('/')

            return render(request, 'shop/login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class CreateUserView(View):
    def get(self, request):
        form = UserForm
        return render(request, 'shop/create_user.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            return redirect('login/')
        else:
            return render(request, 'shop/create_user.html', {'form': form})
