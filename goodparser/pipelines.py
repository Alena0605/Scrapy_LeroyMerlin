# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

import os
from urllib.parse import urlparse

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GoodparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        item['features'] = self.process_features(item['term'], item['definition'])
        del item['term'], item['definition']

        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print(f"The item with id {item['_id']} already exists. ")

        return item

    def process_features(self, terms, definitions):
        features = {}
        for i in range(len(terms)):
            try:
                features[terms[i]] = float(definitions[i])
            except ValueError:
                features[terms[i]] = definitions[i]
        return features


class LeroyMerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['_id']}/{os.path.basename(urlparse(request.url).path)}"
