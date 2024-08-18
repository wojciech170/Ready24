import datetime
from itertools import product

from django.utils.text import slugify

from django.contrib.auth.models import User
from django.db import models

VAT_CHOICES = (
    ('0.11', '11%'),
    ('0.24', '24%'),
)


class Tool(models.Model):
    """
    Represents a tool that can be associated with a product.

    Attributes:
        name (str): The unique name of the tool.
    """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Represents a product category.

    Attributes:
        name (str): The name of the category.
        description (str): A brief description of the category.
        slug (str): A unique slug generated from the category name.
    """

    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Saves the category. If no slug is provided, generates one from the category name.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Represents a product in the inventory.

    Attributes:
        name (str): The name of the product.
        stock (int): The quantity of the product in stock.
        netto_price (int): The net price of the product.
        vat (str): The VAT rate applied to the product.
        height (int): The height of the product.
        length (int): The length of the product.
        width (int): The width of the product.
        weight (int): The weight of the product.
        tool (ManyToManyField): The tools associated with this product.
        category (ForeignKey): The category to which the product belongs.
        slug (str): A unique slug generated from the product name.
    """

    name = models.CharField(max_length=128)
    stock = models.IntegerField(default=0)
    netto_price = models.IntegerField(default=0)
    vat = models.CharField(choices=VAT_CHOICES, default=0)
    height = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    tool = models.ManyToManyField(Tool)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Saves the product. If no slug is provided, generates one from the product name.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def calculate_price(self):
        """
        Calculates the gross price of the product by applying the VAT rate to the net price.

        Returns:
            float: The gross price of the product.
        """
        return (self.netto_price * float(self.vat)) + self.netto_price


class Picture(models.Model):
    """
    Represents an image associated with a product.

    Attributes:
        product (ForeignKey): The product to which the image belongs.
        image (ImageField): The image file.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name


class PromoCodes(models.Model):
    """
    Represents a promotional code that provides a discount.

    Attributes:
        code (str): The unique promotional code.
        discount (int): The discount percentage provided by the code.
        expiry_date (date): The date after which the code is no longer valid.
        active (bool): Indicates whether the code is currently active.
    """

    code = models.CharField(max_length=128, unique=True)
    discount = models.IntegerField(default=0)
    expiry_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def expire_check(self):
        """
        Checks if the promotional code has expired. If expired, sets the code as inactive.
        """
        today = datetime.date.today()
        if self.expiry_date <= today:
            self.active = False


class ShoppingCart(models.Model):
    """
    Represents a shopping cart belonging to a user.

    Attributes:
        user (ForeignKey): The user who owns the shopping cart.
        shopping_cart_product (ManyToManyField): The products added to the cart.
        promo_code (ForeignKey): An optional promotional code applied to the cart.
        active (bool): Indicates whether the shopping cart is currently active.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shopping_cart_product = models.ManyToManyField(Product, through='ShoppingCartProduct', related_name='shopping_cart_product')
    promo_code = models.ForeignKey(PromoCodes, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} cart with ID {self.id} ({self.active})"


class ShoppingCartProduct(models.Model):
    """
    Represents the relationship between a shopping cart and a product, with a specified quantity.

    Attributes:
        product (ForeignKey): The product added to the shopping cart.
        shopping_cart (ForeignKey): The shopping cart to which the product is added.
        quantity (int): The quantity of the product in the shopping cart.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.calculate_price() * self.quantity


class Address(models.Model):
    """
    Represents a user's address.

    Attributes:
        user (ForeignKey): The user to whom the address belongs.
        name (str): The name associated with the address.
        street (str): The street address.
        city (str): The city of the address.
        zipcode (str): The postal code of the address.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    zipcode = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.user.username} adress: {self.name}'
