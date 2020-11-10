# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from productitem.models import Item
from itemadapter import ItemAdapter

# crawling pipeline serves to take scrapy return values and set them to the productitem django model
# can also be used for data preprocessing


class CrawlingPipeline(object):
    def process_item(self, item, spider):

        Item.objects.create(
            product_name=item['product_name'],
            product_price=item['product_price'])

        return item
