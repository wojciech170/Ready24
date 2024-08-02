from django.db import migrations
from django.utils.text import slugify


def populate_category_slugs(apps, schema_editor):
    categories = apps.get_model('shop', 'Category')
    for category in categories.objects.all():
        if not category.slug:
            base_slug = slugify(category.name)
            slug = base_slug
            counter = 1
            while categories.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            category.slug = slug
            category.save()


def populate_product_slugs(apps, schema_editor):
    products = apps.get_model('shop', 'Product')
    for product in products.objects.all():
        if not product.slug:
            base_slug = slugify(product.name)
            slug = base_slug
            counter = 1
            while products.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = slug
            product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0003_category_slug_product_slug'),
    ]

    operations = [
        migrations.RunPython(populate_category_slugs),
        migrations.RunPython(populate_product_slugs),
    ]
