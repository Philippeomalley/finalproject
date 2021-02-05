# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import decimal
# useful for handling different item types with a single interface
import re
from productitem.models import Item
from recipes.models import Recipe, RecipeCategory, Ingredient
from itemadapter import ItemAdapter

# crawling pipeline serves to take scrapy return values and set them to the productitem django model
# can also be used for data preprocessing


class DiscountsPipeline(object):
    def process_item(self, item, spider):
        discount_value = clean_discount(item['product_discount'])
        cleaned_discount = clean_price(discount_value)
        item_object = Item.objects.get_or_create(
            product_name=item['product_name'])[0]
        item_object.product_discount = cleaned_discount
        item_object.save()
        return item


class SainsburysPipeline(object):
    def process_item(self, item, spider):
        item_object = Item.objects.get_or_create(
            product_name=item['product_name'])[0]
        item_object.product_price = clean_price(item['product_price'])
        item_object.product_photo = item['product_photo']
        item_object.save()
        return item


class CategoryPipeline(object):
    def process_item(self, item, spider):
        for category in item['categories']:
            # get or create method: check django db if it exists and if not create it. created is set to true or False
            category_object, created = RecipeCategory.objects.get_or_create(
                category_name=category)
        return item


class IngredientPipeline(object):
    def process_item(self, item, spider):
        for ingredient in item['ingredients']:
            ingredient_object, created = Ingredient.objects.get_or_create(
                ingredient_name=ingredient)
        return item


class RecipePipeline(object):
    def process_item(self, item, spider):
        recipe = Recipe()
        recipe.recipe_name = item['title']
        recipe.recipe_link = item['link']
        recipe.recipe_rating = item['rating']
        recipe.recipe_numRatings = item['numRatings']
        recipe.recipe_image = item['image']
        recipe.recipe_NumServings = item['numServings']
        recipe.save()

        for ingredient in item['ingredients']:
            temp_ingredient = Ingredient.objects.get(
                ingredient_name=ingredient)
            recipe.ingredients.add(temp_ingredient)
        for category in item['categories']:
            temp_category = RecipeCategory.objects.get(
                category_name=category)
            recipe.recipe_category.add(temp_category)
        recipe.save()

        return item

# def process_item(self, item, spider):

#     Ingredient.objects.create(
#         ingredient_name=item['product_name'],
#         product_price=item['product_price'])

#     return item

# def process_item(self, item, spider):

#     Item.objects.create(
#         product_name=item['product_name'],
#         product_price=item['product_price'])

#     return item


def clean_price(price):
    if "p" in price:
        price = re.sub('p', '', price)
        price = decimal.Decimal(price) / 100
    elif "£" in price:
        price = re.sub('£', '', price)
        price = decimal.Decimal(price)
    return price


def clean_discount(discount):
    discount = discount.lower()
    if 'save' in discount:
        discount = discount.split('save', maxsplit=1)[-1]\
            .split(maxsplit=1)[0]
    elif 'half price' in discount:
        discount = discount.split('now', maxsplit=1)[-1]\
            .split(maxsplit=1)[0]
    discount = re.sub(':', '', discount)
    return discount
