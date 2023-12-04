from django.urls import path
from .views import search_recipes, search_results, recipe_detail, my_view

urlpatterns = [
    path('', my_view, name='homepage'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('search/', search_recipes, name='search_recipes'),
    path('search/', search_results, name='search_results'),
    path('api/search_recipes/', search_recipes, name='search_recipes'),
]
