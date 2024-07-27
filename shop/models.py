import datetime

from django.contrib.auth.models import User
from django.db import models


VAT_CHOICES = (
    ('11', '11'),
    ('24', '24'),
)


class Tool(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    stock = models.IntegerField(default=0)
    netto_price = models.IntegerField(default=0)
    vat = models.IntegerField(choices=VAT_CHOICES, default=0)
    height = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    tool = models.ManyToManyField(Tool)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Picture(models.Model):
    filename = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename


class PromoCodes(models.Model):
    code = models.CharField(max_length=128, unique=True)
    discount = models.IntegerField(default=0)
    expiry_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def expire_check(self):
        today = datetime.date.today()
        if self.expiry_date <= today:
            self.active = False


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='ShoppingCartProduct', related_name='shopping_cart_product')
    promo_code = models.ForeignKey(PromoCodes, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


class ShoppingCartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    zipcode = models.CharField(max_length=128)
