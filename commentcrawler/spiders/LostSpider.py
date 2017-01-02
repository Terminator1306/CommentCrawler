#coding:utf-8
import scrapy
import re
from commentcrawler.items import *
import json
import MySQLdb

class LostSpider(scrapy.Spider):
    # name = "lost"
    # allowed_domains = ["jd.com","3.cn"]
    # db = MySQLdb.connection("127.0.0.1","root","","tmall")
    # custom_settings = {
    #  'ITEM_PIPELINES':{'lostPipeline': 300},
    # }
    
    # def start_requests(self):
        # c = db.cursor()
        # c.execute("select product_id,url from lost where valid = '1'")
        # for lost in c.fetchall():
        #     yield scrapy.Request(lost[1],callback=self.parse,meta={'product_id':lost[0]})


    def parse(self, response):
        product_id = response.meta['product_id']
        sel = scrapy.Selector(response)
        body = sel.xpath('//body').extract()
        try :
            if len(body)>0:
                mstr1 = re.sub('<.*?>','',str(body))[11+len('fetchJSON_comment98('):-4].encode('utf-8')
                mstr3 = re.sub(r"\\uff1a",r":",mstr1)
                mstr = re.sub(r"\\x26([a-zA-Z]{2,6});", r"&\1;", mstr3)
                mjson = json.loads(mstr)
                for i in mjson['comments']:
                    comment = Comment()
                    comment['item_type'] = 'comment'
                    comment['content'] = i['content']
                    comment['product_id'] = product_id
                    comment['comment_id'] = i['id']
                    comment['referenceName'] = i['referenceName'] 
                    comment['creationTime'] = i['creationTime']
                    # comment['attribute'] = {}
                    # comment['attribute']['userlevel'] = i['userLevelName'] 
                    # comment['attribute']['usefulVoteCount'] = i['usefulVoteCount']
                    # comment['attribute']['uselessVoteCount'] = i['uselessVoteCount']
                    # comment['attribute']['userProvince'] = i['userProvince']
                    # comment['attribute']['score'] = i['score']
                    # comment['attribute']['userRegisterTime'] = i["userRegisterTime"]
                    comment['userlevel'] = i['userLevelName'] 
                    comment['usefulVoteCount'] = i['usefulVoteCount']
                    comment['uselessVoteCount'] = i['uselessVoteCount']
                    comment['userProvince'] = i['userProvince']
                    comment['score'] = i['score']
                    comment['userRegisterTime'] = i["userRegisterTime"]
                    yield comment
        except Exception,e:
            pass 