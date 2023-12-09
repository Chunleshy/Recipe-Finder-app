from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Recipe
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
        print(form.errors)

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            # Handle authentication failure
            pass

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def protected_view(request):
    # This view can only be accessed by authenticated users
    return render(request, 'protected.html')

@login_required
def my_view(request):
    return render(request, 'index.html')

@login_required
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

@login_required
def get_recipe_details(request):
    recipe_id = request.GET.get('id')
    recipe = get_object_or_404(Recipe, id=recipe_id)

    
    recipe_details = {
        'title': recipe.title,
        'image': recipe.image.url if recipe.image else '',
        'ingredients': recipe.ingredients.split('\n'),  
        'instructions': recipe.instructions,
    }

    return JsonResponse(recipe_details)

