import scrapy
from productitem.models import Item
from recipes.models import Recipe, RecipeCategory, Ingredient
from scrapy_djangoitem import DjangoItem


class ProductItem(DjangoItem):
    django_model = Item


class Category(DjangoItem):
    django_model = RecipeCategory


class Ingredient(DjangoItem):
    django_model = Ingredient


class Recipe(DjangoItem):
    django_model = Recipe
