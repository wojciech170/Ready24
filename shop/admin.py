from django.contrib import admin

# Register your models here.
from .models import (
    Product,
    Tool,
    Category,
    Picture,
    PromoCodes,
    ShoppingCart,
    User
)

admin.site.register(Product)
admin.site.register(Tool)
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(PromoCodes)
admin.site.register(ShoppingCart)
admin.site.register(User)

