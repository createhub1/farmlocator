from django.db import models
from django.contrib.auth.models import User 
from farmer.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.CharField(max_length=1020, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.product.product_name} in {self.user.username}'s cart"
    
class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    
    def __str__(self):
        return f"{self.user}--{self.product}"
    