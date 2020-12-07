from django.shortcuts import render
from django.http import HttpResponse
from productitem.models import Item
from recipes.models import Recipe, RecipeCategory, Ingredient
from django.core import serializers
from .serializers import RecipeSerializer
from django.db import models
import json


from pages.testmatch import test_function, set_coef, recipe_2_json
# Create your views here.
# A view is where you tell django what to do/display


def home_view(request, *args, **kwargs):
    # if request.method == 'POST' and 'run_script' in request.POST:
    #     # import function to run
    # Recipe.objects.all().delete()
    # RecipeCategory.objects.all().delete()
    # Ingredient.objects.all().delete()

    # call function
    # test_function()
    # set_coef()
    # print("done")
    # return user to required page
    return render(request, "home.html", {})


def recipe_gen_view(request, *args, **kwargs):
    # queryset = Recipe.objects.filter(
    #     recipe_category__category_name="Main course").order_by("sort_coefficient")
    # querylist = list(queryset.values())
    # print(recipe_2_json())
    # context = {
    #     'ordered_recipe_list': queryset,
    #     'list': querylist

    # }
    data = recipe_2_json()
    data = json.dumps(data)
    print(data)

    return render(request, "recipe.html",  {'recipe_list': data})
