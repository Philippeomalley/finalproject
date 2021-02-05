from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from productitem.models import Item
from recipes.models import Recipe, RecipeCategory, Ingredient
from django.core import serializers

from .forms import UserRegistrationForm
from django.db import models
import json
from recipes.forms import RecipeCategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import re


from pages.testmatch import matching_function, set_sort_coef
# Create your views here.
# A view is where you tell django what to do/display


def home_view(request, *args, **kwargs):
    # home view displays search form
    if request.GET.getlist('categories') or request.GET.getlist('optimisations'):
        # if form is filled out pull relevant data and redirect
        search_input = request.GET.getlist('categories')
        request.session['search_input'] = search_input
        search_optimisations = request.GET.getlist('optimisations')
        request.session['search_optimisations'] = request.GET.getlist(
            'optimisations')
        return redirect('catalogue')
    return render(request, "home.html")


def recipe_detail_view(request, pk):
    # primary key of recipe is passed through URL
    recipe = Recipe.objects.get(id=pk)
    if request.POST:
        if request.user.is_authenticated:
            request.user.recipes.add(recipe)
            messages.success(
                request, f'{recipe.recipe_name} has been saved')
        else:
            messages.success(
                request, 'you must be logged in to save recipes')
    return render(request, "detail.html",  {'recipe': recipe})


@login_required()
def user_recipes_view(request, *args, **kwargs):
    queryset = request.user.recipes.all()
    context = {
        'ordered_recipe_list': queryset,
    }
    return render(request, "userRecipes.html",  {'context': context})


def catalogue_view(request, *args, **kwargs):

    search_input = request.session.get('search_input')
    optimisations = request.session.get('search_optimisations')
    queryset = Recipe.objects.all()
    for search_category in search_input:
        print(search_category)
        queryset = queryset.filter(
            recipe_category__category_name=search_category)
    set_sort_coef(optimisations, queryset)
    queryset = queryset.order_by('sort_coefficient')
    context = {
        'ordered_recipe_list': queryset,
    }
    return render(request, "catalogue.html",  {'context': context})


def register_view(request, *args, **kwargs):
    # if the request is POST use django's form validators
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # messsages displayed through base.html
            messages.success(
                request, f'{username}\'s account has been created')
            return redirect('login')
    register_form = UserRegistrationForm()
    return render(request, "register.html", {'form': register_form})

# def compare_price():
    # print(Recipe.objects.get(recipe_link = "https://www.bbcgoodfood.com/recipes/chicken-pasta-bake").cost_per_serving)
    # linksList = ["https://www.bbcgoodfood.com/recipes/spanish-meatball-butter-bean-stew","https://www.bbcgoodfood.com/recipes/chilli-con-carne-recipe","https://www.bbcgoodfood.com/recipes/next-level-tikka-masala","https://www.bbcgoodfood.com/recipes/veggie-fajitas","https://www.bbcgoodfood.com/recipes/chicken-pasta-bake","https://www.bbcgoodfood.com/recipes/yaki-udon","https://www.bbcgoodfood.com/recipes/pasta-salmon-peas","https://www.bbcgoodfood.com/recipes/big-batch-bolognese","https://www.bbcgoodfood.com/recipes/double-bean-roasted-pepper-chilli","https://www.bbcgoodfood.com/recipes/cheesy-seafood-bake","https://www.bbcgoodfood.com/recipes/naan-bread-pizza","https://www.bbcgoodfood.com/recipes/chorizo-mozzarella-gnocchi-bake","https://www.bbcgoodfood.com/recipes/satay-sweet-potato-curry","https://www.bbcgoodfood.com/recipes/vegan-banana-bread","https://www.bbcgoodfood.com/recipes/vegan-chilli"]
    # var1 = 0
    # i=0
    # appRecipeList = ["Thai pork & peanut curry","Coconut & squash dhansak","Greek lamb with orzo","Crispy Greek-style pie","Gnocchi & tomato bake", "Hearty pasta soup"]
    # for link in linksList:
    #     try:
    #         var1 += Recipe.objects.get(recipe_link = link).cost_per_serving
    #         print(var1)
    #     except:
    #         print("this one doesn't work: " + link)
    #         i +=1
    # var1 = var1/(len(linksList) - i)
    # print("this is average: " + str(var1))

    # var2 = 0
    # j=0
    # for recipename in appRecipeList:
    #     try:
    #         var1 += Recipe.objects.get(recipe_name = recipename).cost_per_serving
    #         print(var1)
    #     except:
    #         print("this one doesn't work: " + link)
    #         j +=1
    # var1 = var1/(len(appRecipeList) - j)
    # print("this is average: " + str(var1))


# clean_product_name()
    # matching_function()
    # test()
    # token_match_no_clean()
    # levenstein_match_no_clean()
    # if request.method == 'POST' and 'run_script' in request.POST:
    #     # import function to run
    # Item.objects.all().delete()
    # RecipeCategory.objects.all().delete()
    # Ingredient.objects.all().delete()

    # var4 = Recipe.objects.get(recipe_name = "")
    # call function
    # test_function()
    # set_coef()
    # print("done")
    # return user to required page
    # return render(request, "home.html", {})
    # data = recipe_2_json()
    # data = json.dumps(data)
    # matching_function()
    # for recipe in Recipe.objects.all():
    #     recipe.discount_total = 0
    #     for ingredient in recipe.ingredients.all():
    #         for product in ingredient.equivalent_product.all():
    #             recipe.discount_total += product.product_discount
    #     print(recipe.recipe_name)
    #     print(recipe.discount_total)

    # print(request.GET.getlist('categories'))
