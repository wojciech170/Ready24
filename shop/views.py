from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Product
from .forms import LoginForm, UserForm, SearchForm

from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()

# Retrieve all categories to be available globally in the views.
categories = Category.objects.all()


class IndexView(View):
    """
    Handles the rendering of the homepage or base template.

    Methods:
    --------
    GET:
        - Functionality:
            - Passes the list of categories to the template context.
            - Renders the `shop/base.html` template, typically serving as the homepage.

    Template:
    ---------
    - shop/base.html
    """

    def get(self, request):
        return render(request, "shop/base.html", {"categories": categories})


class SearchView(View):
    """
    Handles the search functionality for products.

    Methods:
    --------
    GET:
        - Functionality:
            - Creates a new instance of the `SearchForm`.
            - Passes the form and the list of categories to the template context.
            - Renders the `shop/search.html` template.

    POST:
        - Parameters:
            - searched (str): The search query provided by the user via the search form.
        - Functionality:
            - Validates the search form data.
            - If valid:
                - Attempts to filter products whose names contain the search query (case-insensitive).
                - Passes the search form, filtered products, and list of categories to the template context.
                - Renders the `shop/search.html` template with the search results.
            - If no products match the search query or another error occurs:
                - Passes the search form and list of categories to the template context without products.
                - Renders the `shop/search.html` template.

    Template:
    ---------
    - shop/search.html
    """

    def get(self, request):
        form = SearchForm()
        ctx = {
            'form': form,
            'categories': categories,
        }
        return render(request, "shop/search.html", ctx)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                products = Product.objects.filter(name__icontains=form.cleaned_data['searched'])
                ctx = {
                    'form': form,
                    'products': products,
                    'categories': categories,
                }
                return render(request, "shop/search.html", ctx)
            except Product.DoesNotExist:
                ctx = {
                    'form': form,
                    'categories': categories,
                }
                return render(request, "shop/search.html", ctx)


class CategoryView(View):
    """
    Handles displaying all products under a specific category.

    Methods:
    --------
    GET:
        - Parameters:
            - slug (str): The unique slug of the category to be displayed.
        - Functionality:
            - Retrieves the category object using the provided slug.
            - Fetches all products associated with this category.
            - Passes the list of categories, the specific category, and its products to the template context.
            - Renders the `shop/category.html` template.
        - Error Handling:
            - If the category does not exist, raises a `Http404` error with the message "Category does not exist".

    Template:
    ---------
    - shop/category.html
    """

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
    """
    Handles displaying detailed information about a specific product.

    Methods:
    --------
    GET:
        - Parameters:
            - slug (str): The unique slug of the product to be displayed.
        - Functionality:
            - Retrieves the product object using the provided slug.
            - Passes the product and list of categories to the template context.
            - Renders the `shop/product.html` template.

    Template:
    ---------
    - shop/product.html
    """

    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        ctx = {
            "product": product,
            "categories": categories,
        }
        return render(request, "shop/product.html", ctx)


class LoginView(View):
    """
    Handles user authentication.

    Methods:
    --------
    GET:
        - Functionality:
            - Creates a new instance of the `LoginForm`.
            - Passes the form and the list of categories to the template context.
            - Renders the `shop/login.html` template.

    POST:
        - Parameters:
            - username (str): The username provided by the user.
            - password (str): The password provided by the user.
        - Functionality:
            - Validates the form data.
            - If valid, attempts to authenticate the user using the provided credentials.
            - If authentication is successful, logs the user in and redirects to the home page.
            - If authentication fails, redisplays the login form with an appropriate error message.

    Template:
    ---------
    - shop/login.html
    """

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
    """
    Handles logging out the currently authenticated user.

    Methods:
    --------
    GET:
        - Functionality:
            - Logs out the user.
            - Redirects to the home page after successful logout.

    Template:
    ---------
    - None (redirects to the home page).
    """

    def get(self, request):
        logout(request)
        return redirect('/')


class CreateUserView(View):
    """
    Handles user registration.

    Methods:
    --------
    GET:
        - Functionality:
            - Creates a new instance of the `UserForm`.
            - Passes the form and the list of categories to the template context.
            - Renders the `shop/create_user.html` template.

    POST:
        - Parameters:
            - username (str): The desired username.
            - password1 (str): The desired password.
            - password2 (str): Confirmation of the desired password.
            - email (str): The user's email address.
            - first_name (str): The user's first name.
            - last_name (str): The user's last name.
        - Functionality:
            - Validates the form data.
            - If valid, creates a new user with the provided data.
            - Redirects to the login page after successful registration.
            - If validation fails, redisplays the registration form with the appropriate error messages.

    Template:
    ---------
    - shop/create_user.html
    """

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
