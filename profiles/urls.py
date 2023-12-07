from django.urls import path
from .views import search_recipes, my_view, get_recipe_details

urlpatterns = [
    path('', my_view, name='homepage'),
    path('search/', search_recipes, name='search_recipes'),
    path('api/search_recipes/', search_recipes, name='search_recipes'),
    path('api/get_recipe_details/', get_recipe_details, name='get_recipe_details'),
]
