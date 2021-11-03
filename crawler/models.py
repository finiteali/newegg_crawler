from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=25, null=True)
    code = models.CharField(max_length=40)
    deal_price = models.FloatField(null=True)
    seller = models.CharField(max_length=255)
    main_price = models.FloatField(null=True)
    stars = models.FloatField(null=True)
    count = models.IntegerField(null=True)
    main_image = models.CharField(max_length=1000)
    create = models.DateTimeField(auto_now_add=True)


class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
