# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from productitem.models import Item
from recipes.models import Recipe, RecipeCategory, Ingredient
from itemadapter import ItemAdapter

# crawling pipeline serves to take scrapy return values and set them to the productitem django model
# can also be used for data preprocessing


class SainsburysPipeline(object):
    def process_item(self, item, spider):

        Item.objects.create(
            product_name=item['product_name'],
            product_price=item['product_price'])

        return item


class CategoryPipeline(object):
    def process_item(self, item, spider):
        category = RecipeCategory()
        category.category_name = item['category']
        category.save()
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
