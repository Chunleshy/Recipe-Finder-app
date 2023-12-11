from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, ContentType, Group

class MyPermissions:
    CAN_ACCESS_APP = 'can_access_app'

    @classmethod
    def get_permissions(cls):
        content_type = ContentType.objects.get_for_model(CustomUser)
        return [
            Permission.objects.get_or_create(
                codename=cls.CAN_ACCESS_APP,
                content_type=content_type,
            )[0]
        ]

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

class Recipe(models.Model):
    api_id = models.CharField(max_length=255, unique=True, default='')
    title = models.CharField(max_length=255)
    ingredients = models.TextField(default='')
    instructions = models.TextField(default='')
    saved_by_users = models.ManyToManyField(CustomUser, related_name='saved_recipes', blank=True)

    def __str__(self):
        return self.title

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Favorite: {self.recipe.title}"
