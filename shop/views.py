from venv import create

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category, Product, Tool, Address, ShoppingCart, ShoppingCartProduct
from .forms import LoginForm, UserForm, SearchForm, AddressForm

from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()


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
        return render(request, "shop/base.html")


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
                    # 'categories': categories,
                }
                return render(request, "shop/search.html", ctx)
            except Product.DoesNotExist:
                ctx = {
                    'form': form,
                }
                return render(request, "shop/search.html", ctx)


class CategoryView(View):
    """
    Handles displaying all products under a specific category with filtering by tools.

    Methods:
    --------
    GET:
        - Parameters:
            - slug (str): The unique slug of the category to be displayed.
        - Functionality:
            - Retrieves the category object using the provided slug.
            - Fetches all tools associated with the products in this category.
            - Fetches all products associated with this category.
            - Optionally filters the products by the tools selected via GET parameters.
            - Prepares the context (`ctx`) with:
                - A list of all categories (for navigation or other purposes).
                - The specific category object.
                - The filtered list of products.
                - The list of tools available in the category.
                - The list of selected tool IDs.
            - Renders the `shop/category_view.html` template with the prepared context.
        - Error Handling:
            - If the category does not exist, raises an `Http404` error with the message "Category does not exist".

    Template:
    ---------
    - shop/category_view.html
    """

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            tools = Tool.objects.filter(product__category=category).distinct()
            products = Product.objects.filter(category=category)
            selected_tools = request.GET.getlist('tools')

            if selected_tools:
                for tool_id in selected_tools:
                    products = products.filter(tool__id=tool_id)

            ctx = {
                "category": category,
                "products": products.distinct(),
                "tools": tools,
                "selected_tools": list(map(int, selected_tools)),
            }
            return render(request, "shop/category_view.html", ctx)
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
            - Renders the `shop/product_view.html` template.

    Template:
    ---------
    - shop/product_view.html
    """

    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        ctx = {
            "product": product,
        }
        return render(request, "shop/product_view.html", ctx)


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
        return render(request, 'shop/login.html', {'form': form})

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
        return render(request, 'shop/create_user.html', {'form': form})

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


class ProfileView(LoginRequiredMixin, View):
    """
    Handles displaying a user's profile, including their addresses.

    Inherits:
    ----------
    - LoginRequiredMixin: Ensures that the user is authenticated before accessing this view.

    Attributes:
    ----------
    - login_url (str): The URL to redirect to if the user is not authenticated.

    Methods:
    --------
    GET:
        - Parameters:
            - request (HttpRequest): The incoming HTTP request object.
            - username (str): The username of the user whose profile is to be displayed.
        - Functionality:
            - Retrieves the `User` object based on the provided username.
            - Fetches all addresses associated with the user.
            - Prepares the context (`ctx`) with:
                - The `User` object.
                - A list of all categories (for navigation or other purposes).
                - The list of addresses associated with the user.
            - Renders the `shop/profile_view.html` template with the prepared context.
        - Error Handling:
            - If the user with the provided username does not exist, this view may raise a `User.DoesNotExist` exception.

    Template:
    ---------
    - shop/profile_view.html
    """

    login_url = '/login'

    def get(self, request, username):
        user = User.objects.get(username=username)
        addresses = Address.objects.filter(user=user)
        ctx = {
            "user": user,
            "addresses": addresses,
        }
        return render(request, 'shop/profile_view.html', ctx)


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, username):
        user = User.objects.get(username=username)
        form = UserForm
        ctx = {
            "user": user,
            "form": form,
        }
        return render(request, 'shop/edit_profile.html', ctx)

    def post(self, request, username):
        user = User.objects.get(username=username)
        form = UserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            return redirect(f'/profile/{user.username}')


class AddAddressView(LoginRequiredMixin, View):
    """
    Handles adding a new address for a user.

    Inherits:
    ----------
    - LoginRequiredMixin: Ensures that the user is authenticated before accessing this view.

    Attributes:
    ----------
    - login_url (str): The URL to redirect to if the user is not authenticated.

    Methods:
    --------
    GET:
        - Parameters:
            - request (HttpRequest): The incoming HTTP request object.
            - username (str): The username of the user for whom the address is being added.
        - Functionality:
            - Initializes a blank `AddressForm` for creating a new address.
            - Prepares the context (`ctx`) with:
                - The `AddressForm` instance.
                - A list of all categories (for navigation or other purposes).
                - The username of the user for whom the address is being added.
            - Renders the `shop/add_address.html` template with the prepared context.

    POST:
        - Parameters:
            - request (HttpRequest): The incoming HTTP request object containing the form data.
            - username (str): The username of the user for whom the address is being added.
        - Functionality:
            - Retrieves the `User` object based on the provided username.
            - Initializes an `AddressForm` with the POST data.
            - Validates the form data. If valid:
                - Creates a new `Address` object associated with the user.
                - Saves the new address to the database.
            - Redirects to the user's profile page after successfully adding the address.
        - Error Handling:
            - If the user with the provided username does not exist, this view may raise a `User.DoesNotExist` exception.

    Template:
    ---------
    - shop/add_address.html
    """

    login_url = '/login'

    def get(self, request):
        form = AddressForm()
        ctx = {
            "form": form,
        }
        return render(request, 'shop/add_address.html', ctx)

    def post(self, request):
        user = request.user
        form = AddressForm(request.POST)
        if form.is_valid():
            address = Address.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                city=form.cleaned_data['city'],
                zipcode=form.cleaned_data['zipcode'],
                street=form.cleaned_data['street'],
            )
            address.save()
        return redirect(f'/profile/{user.username}')


class AddToCartView(LoginRequiredMixin, View):
    """
    Handles adding a product to the user's shopping cart.

    Inherits:
    ----------
    - LoginRequiredMixin: Ensures that the user is authenticated before accessing this view.

    Attributes:
    ----------
    - login_url (str): The URL to redirect to if the user is not authenticated.

    Methods:
    --------
    POST:
        - Parameters:
            - request (HttpRequest): The incoming HTTP request object containing the form data.
        - Functionality:
            - Retrieves the `Product` object based on the `product_id` provided in the POST data.
            - Gets or creates an active `ShoppingCart` object for the current user.
            - Gets or creates a `ShoppingCartProduct` object linking the product to the cart.
            - If the product is already in the cart, increments the quantity by 1.
            - Saves the cart item to the database.
            - Redirects the user to their cart page after successfully adding the product.
        - Error Handling:
            - If the product with the provided `product_id` does not exist, raises a `Http404` error.

    Template:
    ---------
    - This view does not directly render a template but redirects to the user's cart page.
    """

    login_url = '/login'

    def post(self, request):
        product_id = request.POST['product_id']
        product = get_object_or_404(Product, pk=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=request.user, active=True)

        cart_item, created = ShoppingCartProduct.objects.get_or_create(shopping_cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect(f'/profile/{request.user.username}/cart')


class CartView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, username):
        cart = get_object_or_404(ShoppingCart, user=request.user, active=True)
        print(cart)
        print(cart.shopping_cart_product.all())
        for item in cart.shopping_cart_product.all():
            print(item)
            print(item.calculate_price())
        return render(request, 'shop/cart_view.html', {'cart': cart})
