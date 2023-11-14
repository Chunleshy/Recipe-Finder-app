from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import IngredientForm
from .models import Ingredient, Recipe
import requests


# Create your views here.
#defines views and forms for user registration
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def signup_view(request):
    return render(request, 'signup.html')  # Renders the signup.html template

#view to deal with ingredient input
def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_input')
    else:
        form = IngredientForm()

    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_input.html', {'form': form, 'ingredients': ingredients})

#This function searches for recipes using the Edamam API
def search_recipes(request):
    # Get ingredients from the database or form input
    ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]

    # Use the Edamam API to search for recipes
    api_key = 'e09fe9a065ead84d20de770503446b05	—'
    base_url = 'https://api.edamam.com/search'
    params = {
        'q': ' '.join(ingredients),
        'app_id': '50c4c823',
        'app_key': api_key,
    }
    response = requests.get(base_url, params=params)
    recipes = response.json().get('hits', [])

    return render(request, 'recipe_search.html', {'recipes': recipes})


def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_details.html', {'recipe': recipe})

