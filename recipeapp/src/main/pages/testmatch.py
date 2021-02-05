import random
import nltk
import json
import string
from fuzzywuzzy import fuzz
from productitem.models import Item
from recipes.models import Recipe, Ingredient
import re
import decimal


def matching_function():

    i = 0
    testList = []
    for recipe in Recipe.objects.all()[520:1133]:
        recipe.recipe_total = 0
        recipe.discount_total = 0
        for ingredient in recipe.ingredients.all():
            for product in Item.objects.all():
                testDict = {}
                testDict['ingredient_name'] = ingredient.ingredient_name
                testDict['product_name'] = product.product_name
                testDict['ratio'] = fuzz.ratio(
                    clean_ingredient_data(ingredient.ingredient_name), clean_product_data(product.product_name))
                testList.append(testDict)

            testList.sort(key=lambda x: x['ratio'], reverse=True)
            temp_product = Item.objects.get(
                product_name=testList[0]['product_name'])
            ingredient.equivalent_product.add(temp_product)
            ingredient.save()

            recipe.recipe_total += temp_product.product_price
            recipe.discount_total += temp_product.product_discount
            testList = []
            recipe.save()
        recipe.cost_per_serving = recipe.recipe_total / recipe.recipe_NumServings
        recipe.save()


def token_match_no_clean():

    i = 0
    testList = []

    rangex = 0
    rangey = rangex+20
    for ingredient in Ingredient.objects.all()[rangex:rangey]:
        print("first ingredient --------")
        for product in Item.objects.all():
            testDict = {}
            testDict['numMatch'] = 0
            ingredient_tokens = nltk.word_tokenize(
                ingredient.ingredient_name.lower())
            product_tokens = nltk.word_tokenize(
                product.product_name.lower())
            for itoken in ingredient_tokens:
                for ptoken in product_tokens:
                    if ptoken == itoken:
                        testDict['numMatch'] += 1

            testDict['ingredient_name'] = ingredient.ingredient_name
            testDict['itokens'] = ingredient_tokens
            testDict['ptokens'] = product_tokens

            testDict['product_name'] = product.product_name
            testList.append(testDict)

        testList.sort(key=lambda x: x['numMatch'], reverse=True)
        temp_product = Item.objects.get(
            product_name=testList[0]['product_name'])
        print(i)
        i += 1
        print(ingredient.ingredient_name)
        print(testList[0]['itokens'])
        print(testList[0]['ptokens'])
        print(temp_product.product_name)
        testList = []


def levenstein_match():

    i = 0
    testList = []
    data = {}
    data['ingredient_matches'] = []
    rangex = 0
    rangey = rangex+20
    for ingredient in Ingredient.objects.all()[rangex:rangey]:
        print("ingredient --------")
        for product in Item.objects.all():
            testDict = {}
            testDict['ingredient_name'] = ingredient.ingredient_name
            testDict['product_name'] = product.product_name

            testDict['ratio'] = fuzz.ratio(
                clean_ingredient_data(ingredient.ingredient_name), clean_product_data(product.product_name))
            testList.append(testDict)

        testList.sort(key=lambda x: x['ratio'], reverse=True)
        temp_product = Item.objects.get(
            product_name=testList[0]['product_name'])

        print(ingredient.ingredient_name)
        print(clean_ingredient_data(ingredient.ingredient_name))
        print("product ---------")
        print(temp_product.product_name)
        print(clean_product_data(temp_product.product_name))
        print("\n")

        data['ingredient_matches'].append({
            'ingredient': ingredient.ingredient_name,
            'product': temp_product.product_name
        })

        testList = []
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def clean_ingredient_data(text):
    text = text.split(",", 1)
    text = text[0]
    text = text.lower()
    text = re.sub("\([^()]*\)", "", text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\d+ml', '', text)
    text = re.sub('\d+g', '', text)
    text = re.sub('\d+', '', text)
    text = re.sub('tbsp', '', text)
    text = re.sub('tsp', '', text)

    return text


def clean_product_data(text):

    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('sainsburys', '', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\d+ml', '', text)
    text = re.sub('\d+g', '', text)
    text = re.sub('tbsp', '', text)
    text = re.sub('tsp', '', text)

    return text


def set_cost_per_serving():
    for recipe in Recipe.objects.all():
        recipe.cost_per_serving = recipe.recipe_total / recipe.recipe_NumServings
        recipe.save()


def set_sort_coef(search_optimisations, queryset):

    for recipe in queryset:
        print(search_optimisations)
        recipe.sort_coefficient = 0
        cps = {'key': "optimisation1",
               'value': recipe.cost_per_serving}
        discount = {'key': "optimisation2",
                    'value': recipe.discount_total}
        rating = {'key': "optimisation3",
                  'value': recipe.recipe_rating}
        if cps['key'] in search_optimisations:
            recipe.sort_coefficient += cps['value']
        if discount['key'] in search_optimisations:
            recipe.sort_coefficient -= discount['value']
        if rating['key'] in search_optimisations:
            recipe.sort_coefficient -= rating['value']
        print(recipe.sort_coefficient)
        recipe.save()


# def save_coef():
#     recipe.save()

#     # recipe.sort_coefficient = recipe.cost_per_serving - recipe.recipe_rating
#     print(recipe.indicator)
#     # recipe.save()


# def test_match2():
#     # tokenize_ingredients()
#     # clean_product_name()
#     testList = []
#     queryset = Recipe.objects.all()
#     recipes10 = queryset[: 10]
#     products = Item.objects.all()
#     products100 = products[: 100]
#     print('start ...')

#     product_names = [product.cleaned_product_name for product in products]
#     print('before encoding ...')
#     product_embeddings = model.encode(product_names)

#     closest_n = 5

#     for recipe in recipes10:
#         print('recipe ...')
#         ingredient_names = [
#             ingredient.ingredient_name for ingredient in recipe.ingredients.all()]
#         ingredient_embeddings = model.encode(ingredient_names)

#         for ingredient_name, ingredient_embedding in zip(ingredient_names, ingredient_embeddings):
#             print('ingredient...')
#             distances = scipy.spatial.distance.cdist(
#                 [ingredient_embedding], product_embeddings, "cosine")[0]

#             results = zip(range(len(distances)), distances)
#             results = sorted(results, key=lambda x: x[1])

#             print("\n\n======================\n\n")
#             print("Ingredient:", ingredient_name)
#             print("\nTop 5 most similar products:")

#             for idx, distance in results[0:closest_n]:
#                 print(product_names[idx].strip(),
#                       "(Score: %.4f)" % (1-distance))


# def gerfe():

#     results = zip(range(len(distances)), distances)
#     results = sorted(results, key=lambda x: x[1])

#     print("\n\n======================\n\n")
#     print("Ingredient:", ingredient_name)
#     print("\nTop 5 most similar products:")

#     for idx, distance in results[0:closest_n]:
#         print(product_names[idx].strip(),
#               "(Score: %.4f)" % (1-distance))


# def clean_product_name():
#     ingredient_tokens = tokenize_ingredients()
#     # ingredient_set = set(tokenize_ingredients())

#     for product in Item.objects.all():
#         lowercase_product_name = product.product_name.lower()
#         tokenized_product = nltk.word_tokenize(lowercase_product_name)
#         print(tokenized_product)
#         cleaned_product_list = [
#             x for x in tokenized_product if x in ingredient_tokens]
#         product.cleaned_product_name = ' '.join(cleaned_product_list)
#         product.save()


# def tokenize_ingredients():
#     tokens = []
#     for recipe in Recipe.objects.all():
#         for ingredient in recipe.ingredients.all():
#             # cleaned_name = clean_data(ingredient.ingredient_name)
#             # tokens += nltk.word_tokenize(cleaned_name)
#             tokens += nltk.word_tokenize(ingredient.ingredient_name)

#     print(len(tokens))
#     return tokens


# def tokenize_products():
#     tokens = []
#     for recipe in Recipe.objects.all():
#         for ingredient in recipe.ingredients.all():
#             # cleaned_name = clean_data(ingredient.ingredient_name)
#             # tokens += nltk.word_tokenize(cleaned_name)
#             tokens += nltk.word_tokenize(ingredient.ingredient_name)

#     print(len(tokens))
#     return tokens
