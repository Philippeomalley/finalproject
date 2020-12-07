import spacy
import nltk
import json
import string
from fuzzywuzzy import fuzz
from productitem.models import Item
from recipes.models import Recipe, Ingredient
import re
import decimal


def test_function():

    # i = 0
    testList = []
    for recipe in Recipe.objects.all():
        recipe.recipe_total = 0
        for ingredient in recipe.ingredients.all():
            for product in Item.objects.all():
                testDict = {}
                testDict['ingredient_name'] = ingredient.ingredient_name
                testDict['product_name'] = product.product_name
                testDict['ratio'] = fuzz.ratio(
                    clean_data(ingredient.ingredient_name), clean_data(product.product_name))
                testList.append(testDict)

            testList.sort(key=lambda x: x['ratio'], reverse=True)
            temp_product = Item.objects.get(
                product_name=testList[0]['product_name'])
            ingredient.equivalent_product.add(temp_product)
            ingredient.save()
            print(temp_product.product_name)
            print(temp_product.product_price)
            recipe.recipe_total += temp_product.product_price
            testList = []
            # print(recipe.price)
            recipe.save()
        recipe.cost_per_serving = recipe.recipe_total / recipe.recipe_NumServings
        recipe.save()
        # i += 1
        # with open('items' + str(i) + '.json', 'w') as outfile:
        #     json.dump(testList, outfile)


# def clean_price(price):
#     if "p" in price:
#         price = re.sub('p', '', price)
#         price = decimal.Decimal(price) / 100
#     elif "£" in price:
#         price = re.sub('£', '', price)
#         price = decimal.Decimal(price)
#     return price


def clean_data(text):
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('sainsburys', '', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\d+', '', text)
    return text


def remove_ne(string):
    nlp = spacy.load('en')
    document = nlp(string)
    text_no_namedentities = []
    ents = [e.text for e in document.ents]
    for item in document:
        if item.text in ents:
            pass
        else:
            text_no_namedentities.append(item.text)


def set_coef():
    for recipe in Recipe.objects.all():
        recipe.cost_per_serving = recipe.recipe_total / recipe.recipe_NumServings
        recipe.sort_coefficient = recipe.cost_per_serving - recipe.recipe_rating
        recipe.save()


def recipe_2_json():
    recipe_list = []
    for recipe in Recipe.objects.filter(
            recipe_category__category_name="Main course").filter(recipe_numRatings__gte = 200):
        recipe_dict = {}
        recipe_dict['recipe_name'] = recipe.recipe_name
        recipe_dict['recipe_image'] = recipe.recipe_image
        recipe_dict['recipe_link'] = recipe.recipe_link
        recipe_dict['recipe_rating'] = float(recipe.recipe_rating)
        recipe_dict['cost_per_serving'] = float(round(recipe.cost_per_serving, 2))
        recipe_dict['recipe_numRatings'] = recipe.recipe_numRatings
        recipe_dict['recipe_NumServings'] = recipe.recipe_NumServings
        recipe_dict['sort_coefficient'] = float(recipe.sort_coefficient)
        recipe_dict['recipe_total'] = float(recipe.recipe_total)

        recipe_dict['ingredients'] = []
        for ingredient in recipe.ingredients.all():
            ingredient_dict = {}
            ingredient_dict['ingredient_name'] = ingredient.ingredient_name
            ingredient_dict['equivalent_product'] = ingredient.equivalent_product.all()[
                0].product_name
            ingredient_dict['equivalent_product_price'] = float(ingredient.equivalent_product.all()[
                0].product_price)
            recipe_dict['ingredients'].append(ingredient_dict)
        recipe_list.append(recipe_dict)

    recipe_list.sort(key=lambda x: x['sort_coefficient'])
    return recipe_list
