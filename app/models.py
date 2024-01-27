from django.db import models

class ProductItem(models.Model):
    title = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.IntegerField()