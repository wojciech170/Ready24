# Generated by Django 5.0.4 on 2024-08-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', 'populate_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
