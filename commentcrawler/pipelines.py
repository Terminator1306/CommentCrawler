# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import datetime
import pymongo
import MySQLdb
import MySQLdb.cursors
import re
import json
import traceback  

from twisted.enterprise import adbapi
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class Pipeline(object):
 
    def __init__(self):
        # self.server = "127.0.0.1"
        # self.port = 27017
        # client = pymongo.MongoClient(self.server, self.port)
        # self.db = client["crawl"]
        # self.collection = db[self.col]
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'tmall',
            user = 'root',
            passwd = '',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )


    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        # query.addErrback(self.handle_error)
        # if item['item_type'] == 'comment':
        #     if self.db["comment"].find({"product_id":item["product_id"],"comment_id":item["comment_id"]}).count()>0:
        #         DropItem("duplicate")
        #         print "********************************\n\nduplicate\n\n**********************************"
        #     else:
        #         self.db["comment"].insert(dict(item))
        #         print"\n\n\n\n\n\n"
        # elif item['item_type'] == 'product':
        #     # if self.db["product"].find({"product_id":item["product_id"],"model":"unknown"}).count()>0:
        #     #     self.db["product"].remove({"product_id":item["product_id"]})
        #     self.db["product"].insert(dict(item))
        #     print"\n\n\n\n\n\n"
            # else:
            #     DropItem("duplicate")
                # print "********************************\n\nduplicate\n\n**********************************"
        # elif item['item_type'] == 'lost':
        #     if  self.collection.find({"url":item["url"]}).count()>0:
        #         DropItem("duplicate")
        #     else:
        #         self.collection.insert(dict(item))
        #         print"\n\n\n\n\n\n"
        return item


    def _conditional_insert(self, tx, item):
        if item['item_type'] == 'comment':
            sql = "insert into comment (product_id, comment_id, referenceName, creationTime, content, attribute) values ('%s', '%s', '%s', '%s', '%s','%s')"%(item['product_id'],
                item['comment_id'],item['referenceName'],item['creationTime'], item['content'], json.dumps(item['attribute'],ensure_ascii=False))
            # with open("result.txt","w") as f:
            #     f.write(sql.encode('utf-8'))
            tx.execute(sql)
        elif item['item_type'] == 'product':
            sql = "insert into product (product_id, comment_count, brand, model, price, name,category ,commentTag, attribute) values ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')"%(item['product_id'],item['comment_count'],item['brand'],item['model'],item['price'],
            item['name'],item['category'],json.dumps(item['commentTag'],ensure_ascii=False),json.dumps(item['attribute'],ensure_ascii=False))
            tx.execute(sql)
        # elif item['item_type'] == 'lost':
        #     if item['content'] == 'empty page':
        #         sql = "insert into lost (product_id, page, url, valid) values ('%s', '%s', '%s', '%s')"%(item['product_id'],item['page'],item['url'],item['valid'])
        #         tx.execute(sql)
        elif item['item_type'] == 'zol_comment':
            sql = "insert into pos_neg (product_id, good, bad, summary, user, date, helpful, helpless) values ('%s','%s','%s','%s','%s','%s','%s', '%s')" % (item['product_id'], item['good'], item['bad'], item['summary'], item['user'], item['date'], item['helpful'], item['helpless'])
            tx.execute(sql)

 
    def handle_error(self, e):
        # pass
        with open("error.txt","a") as f:
            f.write(str(e))
            f.write('\n\n\n\n')


# class lostPipeline(object):
    