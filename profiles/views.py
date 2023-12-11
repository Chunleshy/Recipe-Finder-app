import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission
from .forms import SignUpForm
from .models import Recipe, MyPermissions


@csrf_exempt
@login_required
@require_GET
def search_recipes(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Search query is empty'}, status=400)

    edamam_app_id = '50c4c823'
    edamam_app_key = '54cd516338eea1cb2dd86a6265f81635'

    # Make a request to the Edamam API
    edamam_url = f'https://api.edamam.com/search?q={query}&app_id={edamam_app_id}&app_key={edamam_app_key}'
    response = requests.get(edamam_url)

    if response.status_code == 200:
        edamam_data = response.json()
        # Process the Edamam data as needed
        recipes = [
            {
                'title': recipe['recipe']['label'],
                'image': recipe['recipe']['image'],
                'url': recipe['recipe']['url']
            }
            for recipe in edamam_data['hits']
        ]
        return JsonResponse(recipes, safe=False)
    else:
        # Handle API request error
        return JsonResponse({'error': 'Failed to fetch recipes from Edamam API'}, status=500)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get the 'Random Users' group
            group = Group.objects.get(name='Random Users')

            # Get the custom permissions
            permissions = MyPermissions.get_permissions()

            # Loop through users in the group and update permissions
            for user in group.user_set.all():
                # Clear existing permissions
                user.user_permissions.clear()

                # Assign the new permissions
                user.user_permissions.set(permissions)

                # Save the user
                user.save()

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
def my_view(request):
    return render(request, 'index.html')
