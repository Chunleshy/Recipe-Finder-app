from django.urls import path
from .views import search_recipes, my_view, get_recipe_details, login_view, logout_view,signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', my_view, name='homepage'),
    path('search/', search_recipes, name='search_recipes'),
    path('api/search_recipes/', search_recipes, name='search_recipes'),
    path('api/get_recipe_details/', get_recipe_details, name='get_recipe_details'),    
]

