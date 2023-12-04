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


def get_edamam_recipes(query):
    # Replace 'your_app_id' and 'your_app_key' with your Edamam API credentials
    edamam_api_url = 'https://api.edamam.com/search'
    app_id = '50c4c823'
    app_key = 'e09fe9a065ead84d20de770503446b05	—'

    params = {
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
    }

    try:
        response = requests.get(edamam_api_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        recipes = []

        for hit in data.get('hits', []):
            recipe_data = hit.get('recipe', {})
            recipes.append({
                'title': recipe_data.get('label', ''),
                'ingredients': recipe_data.get('ingredientLines', []),
                'instructions': recipe_data.get('url', ''),
            })

        return recipes

    except requests.RequestException as e:
        # Handle exceptions such as network errors or invalid responses
        print(f"Error making request to Edamam API: {e}")
        return {'error': 'Error connecting to the Edamam API'}

    except Exception as e:
        # Handle other unexpected exceptions
        print(f"Unexpected error: {e}")
        return {'error': 'An unexpected error occurred'}



def search_results(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})



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
