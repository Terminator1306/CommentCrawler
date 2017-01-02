# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
 
import scrapy

class Product(scrapy.Item):
    item_type = scrapy.Field()
    product_id = scrapy.Field()
    comment_count = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    commentTag = scrapy.Field()
    attribute = scrapy.Field()


class Comment(scrapy.Item):
    item_type = scrapy.Field()
    content = scrapy.Field()
    product_id = scrapy.Field()
    comment_id = scrapy.Field()
    referenceName = scrapy.Field()
    creationTime = scrapy.Field()
    # userlevel = scrapy.Field()
    # usefulVoteCount = scrapy.Field()
    # uselessVoteCount =scrapy.Field()
    # userProvince = scrapy.Field()
    # score = scrapy.Field()
    # userRegisterTime = scrapy.Field()
    attribute = scrapy.Field()


class Lost(scrapy.Item):
    item_type = scrapy.Field()      
    content = scrapy.Field()
    url = scrapy.Field()
    page = scrapy.Field()
    product_id = scrapy.Field()
    valid = scrapy.Field()



    
        
