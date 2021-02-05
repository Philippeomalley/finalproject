from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# import the scraper and specific spider settings
from scraper.scraper import settings as my_settings
from scraper.scraper.spiders.sainsburys import SainsburysSpider

# base command to run spider - can be run as function or from terminal


class Command(BaseCommand):
    help = 'Release spider'
# handle is the default command function

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(SainsburysSpider)
        process.start()
