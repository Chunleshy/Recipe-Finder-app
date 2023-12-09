from django.contrib import admin
from .models import Recipe, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Recipe)



