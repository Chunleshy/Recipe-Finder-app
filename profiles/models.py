from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField(default='')
    instructions = models.TextField(default='')

    def __str__(self):
        return self.title