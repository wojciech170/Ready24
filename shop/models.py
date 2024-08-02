import datetime
from django.utils.text import slugify

from django.contrib.auth.models import User
from django.db import models

VAT_CHOICES = (
    ('0.11', '11%'),
    ('0.24', '24%'),
)


class Tool(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
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
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def price(self):
        return (self.netto_price * float(self.vat)) + self.netto_price


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name


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

    def __str__(self):
        return f"{self.user.username} cart with ID {self.id} ({self.active})"


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
