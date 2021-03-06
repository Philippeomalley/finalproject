import scrapy
from scraper.scraper.items import ProductItem
# from scrapy.spiders import CrawlSpider


class SainsburysSpider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = "sainsburys"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.scraper.pipelines.SainsburysPipeline': 400
        }}

    groceries_url = "https://www.sainsburys.co.uk/shop/gb/groceries"
    start_urls = [

        groceries_url+"/food-cupboard/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=12422&parent_category_rn=&top_category=12422&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=12422&categoryFacetId2=",
        groceries_url+"/meat-fish/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=13343&parent_category_rn=&top_category=13343&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=13343&categoryFacetId2=",
        groceries_url+"/dairy-eggs-and-chilled/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=428866&parent_category_rn=&top_category=428866&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=428866&categoryFacetId2=",
        groceries_url+"/bakery/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=12320&parent_category_rn=&top_category=12320&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=12320&categoryFacetId2=",
        groceries_url+"/frozen-/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=218831&parent_category_rn=&top_category=218831&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=218831&categoryFacetId2=",
        groceries_url+"/fruit-veg/seeall?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=12518&parent_category_rn=&top_category=12518&pageSize=60&orderBy=FAVOURITES_FIRST&searchTerm=&catSeeAll=true&beginIndex=0&categoryFacetId1=12518&categoryFacetId2="
    ]

    def parse(self, response):
        for item in response.css('li.gridItem'):

            product = ProductItem()
            product['product_name'] = item.css(
                '.productNameAndPromotions a::text').get().strip()
            product['product_price'] = item.css(
                '.pricePerUnit::text').get().strip()
            product['product_photo'] = item.xpath(
                './/div[@class="productNameAndPromotions"]//a//img/@src').extract_first()

            yield product
            next_page = response.css(
                'div.pagination.paginationBottom li.next a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
