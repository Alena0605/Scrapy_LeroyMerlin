import scrapy
from scrapy.http import HtmlResponse
from goodparser.items import GoodparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']")
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodparserItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('term', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('definition', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath('_id', "//span[@slot='article']/@content")
        yield loader.load_item()
