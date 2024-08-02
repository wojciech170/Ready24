from django.http import Http404
from django.shortcuts import render
from django.views import View
from .models import Category, Product


class IndexView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "shop/base.html", {"categories": categories})


class CategoryView(View):
    def get(self, request, slug):
        try:
            categories = Category.objects.all()
            category = Category.objects.get(slug=slug)
            products = Product.objects.filter(category=category)
            ctx= {
                "categories": categories,
                "category": category,
                "products": products
            }
            return render(request, "shop/category.html", ctx)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")

