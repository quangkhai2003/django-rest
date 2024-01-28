from django.db import models

class ProductItem(models.Model):
    title = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.IntegerField()
    
    def __str__(self):
        return self.title
    
class CartItem(models.Model):
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"