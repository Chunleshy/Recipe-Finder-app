from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):    
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        app_label = 'profiles'
## Explicitly define related names for groups and user_permissions
CustomUser.groups.field.remote_field.related_name = 'customuser_groups'
CustomUser.user_permissions.field.remote_field.related_name = 'customuser_user_permissions'

#Model to create user profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ##profile_picture = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')

#Model to represent ingredients
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
#model to represent recipes
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    # Add other fields as needed (instructions, image,...)

    def __str__(self):
        return self.title
