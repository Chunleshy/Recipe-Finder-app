from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

# Create your models here.

DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('difficult', 'Difficult'),
]


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
    category = models.CharField(max_length=50, blank=True)

    
    def __str__(self):
        return self.name
    
#model to represent recipes
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField(default='Add recipe instruction here.') #text field to store step by step instructions for preparing the recipe 
    cooking_time = models.DurationField(null=True, blank=True)
    preparation_time = models.DurationField(null=True, blank=True)
    servings = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
   
    def __str__(self):
        return self.title
