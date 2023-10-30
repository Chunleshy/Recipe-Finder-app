from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):    
    bio = models.TextField(max_length=500, blank=True)
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ##profile_picture = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
