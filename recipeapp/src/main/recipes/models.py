from django.db import models
from productitem.models import Item


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    equivalent_products = models.ManyToManyField(Item, through="ingredientMap")

    def __str__(self):
        return self.ingredient_name


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255, unique=True)
    recipe_total = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    # the django manyToMany model automatically creates
    # third table that ties recipe and ingredients table together
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.recipe_name


class IngredientMap(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    matching_ratio = models.DecimalField(max_digits=20, decimal_places=10)
