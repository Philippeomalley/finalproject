from django.db import models
from productitem.models import Item
from django.contrib.auth.models import User

# If I want to have a shortlist of equivalent products - extend many to many relationship through
# IngredientMap model which can be ordered by matching ratio


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    # equivalent_products = models.ManyToManyField(Item, through="ingredientMap")
    equivalent_product = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.ingredient_name


class RecipeCategory(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    recipe_total = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    discount_total = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    recipe_link = models.CharField(max_length=255, unique=True)
    recipe_rating = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    recipe_numRatings = models.IntegerField()
    recipe_image = models.CharField(max_length=255)
    recipe_category = models.ManyToManyField(RecipeCategory)
    recipe_NumServings = models.IntegerField()
    cost_per_serving = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    sort_coefficient = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    # the django manyToMany model automatically creates
    # third table that ties recipe and ingredients table together
    ingredients = models.ManyToManyField(Ingredient)
    # diets = models.ManyToManyField(Diet)
    users = models.ManyToManyField('auth.User', related_name='recipes')

    def __str__(self):
        return self.recipe_name


# class IngredientMap(models.Model):
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
#     product = models.ForeignKey(Item, on_delete=models.CASCADE)
#     matching_ratio = models.DecimalField(max_digits=20, decimal_places=10)
