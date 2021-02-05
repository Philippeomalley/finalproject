from django import forms
from .models import RecipeCategory


class RecipeCategoryForm(forms.ModelForm):
    recipe_type_choices = [
        ('Breakfast', 'Breakfast'), ('Main Course', 'Main Course'), ('Snack', 'Snack'), ('Desert', 'Desert')]
    Recipe_Type = forms.ChoiceField(
        choices=recipe_type_choices, widget=forms.RadioSelect())

    class Meta:
        model = RecipeCategory
        fields = '__all__'
