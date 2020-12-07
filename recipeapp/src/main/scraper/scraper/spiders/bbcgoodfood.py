import scrapy
import json
import re
from scraper.scraper.items import Recipe, RecipeCategory, Ingredient
# from scrapy.spiders import CrawlSpider


class RecipeItem(scrapy.Item):
    # define the fields for your item here like
    title = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    ingredients = scrapy.Field()
    image = scrapy.Field()
    categories = scrapy.Field()
    numRatings = scrapy.Field()
    numServings = scrapy.Field()


class BBCGoodFoodSpider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = "bbcgoodfood"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.scraper.pipelines.CategoryPipeline': 400,
            'scraper.scraper.pipelines.IngredientPipeline': 400,
            'scraper.scraper.pipelines.RecipePipeline': 500
        }}

    BASE_URL = 'https://www.bbcgoodfood.com'

    start_urls = [
        "https://www.bbcgoodfood.com/search/recipes/page/%s/?sort=-popular" %
        page for page in range(1, 40)
    ]

    def parse(self, response):
        links = response.css(
            '.standard-card-new__display-title a::attr(href)').extract()
        for link in links:
            url = self.BASE_URL + link
            yield scrapy.Request(url, callback=self.parse_recipe)
        # next_page = response.css(
        #     'a.pagination-arrow--next::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_recipe(self, response):

        recipe_data = json.loads(response.xpath(
            '//script[@type="application/ld+json"]//text()').extract_first())

        recipe = RecipeItem()
        recipe["title"] = recipe_data["name"]
        recipe["link"] = response.request.url
        recipe["image"] = recipe_data["image"]["url"]
        recipe["categories"] = recipe_data["recipeCategory"].split(", ")

        recipe["numServings"] = re.search(
            r'\d+',  str(recipe_data["recipeYield"])).group()
        recipe["ingredients"] = []
        for ingredient in recipe_data["recipeIngredient"]:
            ingredient = re.sub(r'(?<=[.,])(?=[^\s])', r' ', ingredient)
            recipe["ingredients"].append(ingredient)

        ratingExist = response.css(
            '.recipe-template script::text').get() or False
        print(ratingExist)
        if(ratingExist != False):
            rating_data = json.loads(ratingExist)
            recipe["rating"] = rating_data["aggregateRating"]["ratingValue"]
            recipe["numRatings"] = rating_data["aggregateRating"]["reviewCount"]
        else:
            recipe["rating"] = 0
            recipe["numRatings"] = 0

        return recipe
