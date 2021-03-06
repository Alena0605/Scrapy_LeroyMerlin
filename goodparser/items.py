# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def process_price(value):
    try:
        value = value.replace(' ', '')
        value = int(value)
    except Exception as e:
        print(e)
    finally:
        return value


class GoodparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    term = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
    definition = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
    features = scrapy.Field()
    _id = scrapy.Field(output_processor=TakeFirst())
