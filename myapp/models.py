from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('consumer', 'Consumer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='consumer')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    farm_image = models.ImageField(upload_to='farm_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class FAQ(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=1024)
    question = models.TextField()
    
    def __str__(self):
        return self.email