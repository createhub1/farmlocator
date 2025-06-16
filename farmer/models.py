from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=1020)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_image')
    certification = models.ImageField(upload_to='certificates')
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.product_name

class FarmerDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_image')
    farm_name = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.user.username