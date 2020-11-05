import scrapy
from productitem.models import Item
from scrapy_djangoitem import DjangoItem


class ProductItem(DjangoItem):
    django_model = Item
