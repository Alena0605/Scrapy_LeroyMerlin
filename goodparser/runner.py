from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from goodparser.spiders.leroymerlin import LeroymerlinSpider
from goodparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    query = 'книжный шкаф'
    process.crawl(LeroymerlinSpider, query=query)
    process.start()
