import scrapy
from scraper.scraper.items import ProductItem
# from scrapy.spiders import CrawlSpider


class DiscountSpider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = "discounts"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.scraper.pipelines.DiscountsPipeline': 400
        }}

    groceries_url = "https://www.sainsburys.co.uk/shop/gb/groceries"
    start_urls = [
        groceries_url+"/fruit-veg/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=12518&parent_category_rn=&top_category=12518&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=12518&categoryFacetId2="
    ]

    def parse(self, response):
        for item in response.css('li.gridItem .specialOffer'):

            product = ProductItem()
            product['product_name'] = item.css(
                '.productNameAndPromotions a::text').get().strip()
            product['product_discount'] = item.css(
                '.promotion a::text').get()

            yield product
            next_page = response.css(
                'div.pagination.paginationBottom li.next a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
