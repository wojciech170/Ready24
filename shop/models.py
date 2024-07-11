from django.db import models


VAT_CHOICES = (

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
    tool_id = models.ManyToManyField(Tool, through='ProductTool')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class ProductTool(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    Tool = models.ForeignKey(Tool, on_delete=models.CASCADE)


class Picture(models.Model):
    filename = models.CharField(max_length=128)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

