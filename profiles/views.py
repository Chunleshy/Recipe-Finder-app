from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Recipe
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import render
from django.views.decorators.http import require_GET


def my_view(request):
    return render(request, 'index.html')


@require_GET
def search_recipes(request):
    query = request.GET.get('q', '')
    edamam_app_id = '50c4c823'
    edamam_app_key = '54cd516338eea1cb2dd86a6265f81635'

    # Make a request to the Edamam API
    edamam_url = f'https://api.edamam.com/search?q={query}&app_id={edamam_app_id}&app_key={edamam_app_key}'
    response = requests.get(edamam_url)

    if response.status_code == 200:
        edamam_data = response.json()
        # Process the Edamam data as needed
        recipes = [{'title': recipe['recipe']['label'], 'image': recipe['recipe']['image'], 'url': recipe['recipe']['url']} for recipe in edamam_data['hits']]
        return JsonResponse(recipes, safe=False)
    else:
        # Handle API request error
        return JsonResponse({'error': 'Failed to fetch recipes from Edamam API'}, status=500)


def get_recipe_details(request):
    recipe_id = request.GET.get('id')
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Adjust the following based on your model structure
    recipe_details = {
        'title': recipe.title,
        'image': recipe.image.url if recipe.image else '',
        'ingredients': recipe.ingredients.split('\n'),  # Adjust as needed
        'instructions': recipe.instructions,
    }

    return JsonResponse(recipe_details)
