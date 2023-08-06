from scrapy_nc.db import mongo_db
import json
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    def process_item(self, item, spider):
        my_item = item.deepcopy()
        item_dict = dict(my_item)
        unique_id = item['unique_id']
        if not unique_id:
            raise DropItem('unique_id is None')

        crawled_at = item['crawled_at']
        if not crawled_at:
            raise DropItem('crawled_at is None')

        spider.collection.update_one({
            'unique_id':   my_item.get('unique_id')
        }, {"$set": item_dict}, upsert=True)
        return item

    def open_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        spider = crawler.spider
        instance = cls()
        if not mongo_db:
            spider.logger.error('mongodb no configuration')
            return instance
        spider.collection = mongo_db.get_collection(spider.name)
        res = json.dumps(spider.collection.index_information())
        spider.logger.info(
            f'index_information {res}')
        index_name = 'unique_id'
        if index_name not in spider.collection.index_information():
            spider.collection.create_index(
                'unique_id', unique=True, name=index_name)
            spider.logger.info(f"create unique index {index_name}")
        ttl = spider.settings.get('DATA_TTL')
        if ttl is None:
            ttl = 86400 * 30 * 3 # 默认过期时间 90 天
            spider.logger.info(f'not found data_ttl,  set ttl 30 days')
        if ttl == -1:
            return instance
        if ttl > 0:
            expire_index_name = "crawled_at"
            if expire_index_name not in spider.collection.index_information():
                spider.collection.create_index(
                    "crawled_at", name=expire_index_name, expireAfterSeconds=ttl,
                )
                spider.logger.info(f'create ttl index {expire_index_name}, ttl: {ttl}')
        return instance

