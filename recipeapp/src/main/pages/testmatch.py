import spacy
import nltk
import json
import string
from fuzzywuzzy import fuzz
from productitem.models import Item
from recipes.models import Recipe, Ingredient
import re


testArray = ["1 onion", "1 red pepper", "2 garlic cloves", "1 Tbsp oil", "1 heaped tsp hot chilli powder", "1 tsp paprika", "1 tsp ground cumin", "500g lean minced beef",
             "1 beef stock cube", "400g can chopped tomatoes", "½ tsp dried marjoram", "1 tsp sugar", "2 Tbsp tomato purée", "410g can red kidney beans", "long grain rice", "soured cream"]


def test_function():

    # i = 0
    testList = []
    for recipe in Recipe.objects.all():
        recipe.price = 0
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
            # recipe.price += temp_product.product_price
            testList = []
            # print(recipe.price)
            # recipe.save()
        # i += 1
        # with open('items' + str(i) + '.json', 'w') as outfile:
        #     json.dump(testList, outfile)


def print_top10(list):
    for item in list:
        print(item)


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
