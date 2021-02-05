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
            'scraper.scraper.pipelines.CategoryPipeline': 100,
            'scraper.scraper.pipelines.IngredientPipeline': 100,
            'scraper.scraper.pipelines.RecipePipeline': 200
        }}

    BASE_URL = 'https://www.bbcgoodfood.com'

    start_urls = [
        "https://www.bbcgoodfood.com/search/recipes/page/%s/?sort=-popular" %
        page for page in range(1, 2)
    ]

    def parse(self, response):
        links = response.css(
            '.standard-card-new__display-title a::attr(href)').extract()
        # follow each link on the catalogue layout
        for link in links:
            url = self.BASE_URL + link
            yield scrapy.Request(url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        # extract the JSON schema from the script tag that contains it to access relevant data
        data = response.xpath(
            '//script[@type="application/ld+json"]//text()').extract_first()
        recipe_data = json.loads(data)
        recipe = RecipeItem()

        recipe["title"] = recipe_data["name"]
        recipe["link"] = response.request.url
        recipe["image"] = recipe_data["image"]["url"]
        recipe["categories"] = recipe_data["recipeCategory"].split(", ")

        # as these pieces of data aren't always in the same place, the whole schema is searched to find any instances
        vegetarian_matches = ["vegetarian", "Vegetarian"]
        vegan_matches = ["vegan", "Vegan"]
        gluten_matches = ["gluten-free", "Gluten-free", "gluten free"]
        healthy_matches = ["healthy", "Healthy"]

        if any(x in data for x in vegetarian_matches):
            recipe["categories"].append("vegetarian")

        if any(x in data for x in vegan_matches):
            recipe["categories"].append("vegan")

        if any(x in data for x in gluten_matches):
            recipe["categories"].append("gluten free")

        if any(x in data for x in healthy_matches):
            recipe["categories"].append("healthy")

        # extract integer from num servings string
        recipe["numServings"] = re.search(
            r'\d+',  str(recipe_data["recipeYield"])).group()
        recipe["ingredients"] = []
        for ingredient in recipe_data["recipeIngredient"]:
            ingredient = re.sub(r'(?<=[.,])(?=[^\s])', r' ', ingredient)
            recipe["ingredients"].append(ingredient)

        ratingExist = response.css(
            '.post__header script::text').get() or False
        if(ratingExist != False):
            rating_data = json.loads(ratingExist)
            recipe["rating"] = rating_data["aggregateRating"]["ratingValue"]
            recipe["numRatings"] = rating_data["aggregateRating"]["reviewCount"]
        else:
            recipe["rating"] = 0
            recipe["numRatings"] = 0

        return recipe
