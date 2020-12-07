from rest_framework import serializers

from productitem.models import Item
from recipes.models import Recipe, RecipeCategory, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Recipe
        fields = {
            'recipe_name', 'recipe_total'
        }
