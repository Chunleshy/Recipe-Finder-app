from django.urls import path
from .views import SignUp, add_ingredient, search_recipes

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('ingredient_input/', add_ingredient, name='ingredient_input'),
    path('recipe_search/', search_recipes, name='recipe_search'),
    ]
