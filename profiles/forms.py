#This is a form for users to input their ingredients

from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']
