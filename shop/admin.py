from django.contrib import admin

# Register your models here.
from .models import Product, Tool, Category

admin.site.register(Product)
admin.site.register(Tool)
admin.site.register(Category)
