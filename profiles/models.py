from django.db import models

# Create your models here.

#recipe Model

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField(default='')
    instructions = models.TextField(default='')

    def __str__(self):
        return self.title