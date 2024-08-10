from .models import Category


def category_list(request):
    categories = Category.objects.all()
    ctx = {
        'categories': categories
    }
    return ctx
