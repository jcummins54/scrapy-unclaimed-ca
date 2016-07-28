import pymongo
from scrapy.exceptions import DropItem

import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class DataPipeline(object):
    collection_name = 'items'

    def __init__(self, mongo_uri, mongo_db):
        self.ids_seen = set()
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].remove()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['id']:
            if item['id'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['id'])
                self.db[self.collection_name].insert(dict(item))
                return item
        else:
            raise DropItem("Missing id in %s" % item)