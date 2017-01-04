#coding:utf-8
import scrapy
from scrapy.http import Request
import json
import re
import threading,time
from commentcrawler.items import *
import random
import string

class JDSpider(scrapy.Spider):
    name = "JD_SJ"
    allowed_domains = ["jd.com","3.cn","jd.hk"]
    start_urls = [
        # "http://list.jd.com/list.html?cat=652,654,831",
        "http://list.jd.com/list.html?cat=670,671,672"
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        items = sel.xpath('//div[@id="plist"]/ul/li/div/div[1]/a/@href').extract()
        next_page = sel.xpath('//div[@id="J_bottomPage"]/span/a[@class="pn-next"]/@href').extract()
        for i in range(0,len(items)):
            yield Request(
                url="http:"+items[i],
                dont_filter=True,
                callback=self.IteminfoParse,
                )
        if len(next_page)>0:
            yield scrapy.Request(
                url="http://list.jd.com"+next_page[0],
                dont_filter=True,
                callback=self.parse
                )
        with open ("product_pages.txt","a") as f:
            f.write(next_page[0][20:-15]+':'+str(len(items))+'\n')


    def IteminfoParse(self, response):
        # try :
            sel = scrapy.Selector(response)
            dt = sel.xpath('//div[@class="Ptable-item"]//dt/text()').extract()
            dd = sel.xpath('//div[@class="Ptable-item"]//dd/text()').extract()
            info = re.sub("[\\n ]","",sel.xpath('//head/script').extract()[0])
            product_id = re.sub(".*skuid:(.*?)[,\\}].*",'\\1',info)
            brand = re.sub(".*brand:(.*?)[,\\}].*",'\\1',info)
            name = re.sub(".*name:(.*?)[,\\}].*",'\\1',info)[1:-1].decode('unicode-escape')
            # name = sel.xpath('//div[@class="sku-name"]/text()').extract()[0]
            model = "unknown"
            attribute = {}
            
            if len(dt) == 0:
                dt = sel.xpath('//div[@id="detail-param"]//tr/td[1]/text()').extract()
                dd = sel.xpath('//div[@id="detail-param"]//tr/td[2]/text()').extract()

            if len(dt) == 0:
                dt = sel.xpath('//table[@class="Ptable"]//tr/td[1]/text()').extract()
                dd = sel.xpath('//table[@class="Ptable"]//tr/td[2]/text()').extract()

            lenth = len(dd)
            if len(dt)<lenth:
                lenth = len(dt)

            for index in range(0,lenth):
                attribute[dt[index]] = dd[index]
                if dt[index]==u"型号":
                    model = dd[index]

            yield Request(
                    url="http://brand.jd.com/pinpai/%s.html"%(brand,),
                    callback=self.BrandParse,
                    dont_filter=True,
                    meta={
                    'product_id':product_id,
                    'model':model,
                    'name':name,
                    'attribute':attribute
                   }
                )
        # except Exception,e:
        #      with open("result.txt","a") as f:
        #         f.write(str(e)+'\n')


    def BrandParse(self,response):
        sel = scrapy.Selector(response)
        brand = sel.xpath('//a[@class="shop"]/text()').extract()[0]
        product_id = response.meta['product_id']
        yield Request(
                   url="http://p.3.cn/prices/mgets?skuIds=J_%s"%(product_id,),
                   callback=self.PriceParse,
                   dont_filter=True,
                   meta={
                   'product_id':product_id,
                   'brand':brand,
                   'model':response.meta['model'],
                   'name':response.meta['name'],
                   'attribute':response.meta['attribute']
                   }
                )


    def PriceParse(self,response):
        sel = scrapy.Selector(response)
        content = sel.xpath('//body//text()').extract()[0]
        price = re.sub('.*"p":"(.*?)".*','\\1',content)
        product_id = response.meta['product_id']
        yield Request(
                   url="http://sclub.jd.com/productpage/p-%s-s-0-t-3-p-0.html"%(product_id,),
                   callback=self.CommentSummaryParse,
                   dont_filter=True,
                   meta={
                   'product_id':product_id,
                   'brand':response.meta['brand'],
                   'model':response.meta['model'],
                   'name':response.meta['name'],
                   'attribute':response.meta['attribute'],
                   'price':price
                   }
                   )


    def CommentSummaryParse(self,response):
        sel = scrapy.Selector(response)
        body = sel.xpath('//body').extract()[0]
        mstr = re.sub('<.*?>','',str(body).encode('utf-8'))
        mjson = json.loads(mstr)
        product_id = "JD_" + response.meta['product_id']

        product = Product()
        product['category'] = 'laptop'
        product['item_type'] = 'product'
        product['product_id'] = product_id
        product['brand'] = response.meta['brand']
        product['model'] = response.meta['model']
        product['name'] = response.meta['name']
        product['price'] = response.meta['price']
        product['attribute'] = response.meta['attribute']
        product['comment_count'] = comment_count = mjson['productCommentSummary']['commentCount']
        product['attribute']['score1Count'] = mjson['productCommentSummary']['score1Count']
        product['attribute']['score2Count'] = mjson['productCommentSummary']['score2Count']
        product['attribute']['score3Count'] = mjson['productCommentSummary']['score3Count']
        product['attribute']['score4Count'] = mjson['productCommentSummary']['score4Count']
        product['attribute']['score5Count'] = mjson['productCommentSummary']['score5Count']
        product['commentTag'] = {}
        for tag in mjson['hotCommentTagStatistics']:
            product['commentTag'][tag['name']] = tag['count']
        if int(product['comment_count'])>0:
            yield product
            minpage = 100
            maxpage = 1000
            if int(comment_count)<maxpage*10:
                maxpage = int(comment_count)/10
            if int(comment_count)<minpage*10:
                maxpage = minpage = 0
        
            for page in range(0,int(comment_count)/10):
                salt = string.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 2)).replace(' ','')
                salt += str(random.randint(100000,999999))
                yield Request(
                    url="http://sclub.jd.com/productpage/p-%s-s-0-t-3-p-%d.html?callback=fetchJSON_comment98%s"%(product_id[3:],page,salt),
                    callback=self.CommentParse,
                    meta={'product_id':product_id,
                    'page':page,
                    'salt':salt,
                    't':0
                    }
                    )


    def CommentParse(self,response):
        product_id = response.meta['product_id']
        page = response.meta['page']
        salt = response.meta['salt']
        sel = scrapy.Selector(response)
        body = sel.xpath('//body').extract()
        try :
            if len(body)>0:
                mstr1 = re.sub('<.*?>','',str(body))[11+len('fetchJSON_comment98('):-4].encode('utf-8')
                # mstr2 = re.sub(r"\\n", r"", mstr1)
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
                    comment['attribute'] = {}
                    comment['attribute']['userlevel'] = i['userLevelName'] 
                    comment['attribute']['usefulVoteCount'] = i['usefulVoteCount']
                    comment['attribute']['uselessVoteCount'] = i['uselessVoteCount']
                    comment['attribute']['userProvince'] = i['userProvince']
                    comment['attribute']['score'] = i['score']
                    comment['attribute']['userRegisterTime'] = i["userRegisterTime"]
                    # comment['userlevel'] = i['userLevelName'] 
                    # comment['usefulVoteCount'] = i['usefulVoteCount']
                    # comment['uselessVoteCount'] = i['uselessVoteCount']
                    # comment['userProvince'] = i['userProvince']
                    # comment['score'] = i['score']
                    # comment['userRegisterTime'] = i["userRegisterTime"]
                    yield comment
            else:
                lost = Lost()
                lost['item_type'] = 'lost'
                lost['url'] = response.url
                lost['product_id'] = product_id
                lost['page'] = page
                lost['content'] = "empty page"
                lost['valid'] = 1
                # yield lost
        except Exception,e:
            lost = Lost()
            lost['item_type'] = 'lost'
            lost['content'] = str(e)
            lost['product_id'] = product_id
            lost['page'] = page
            lost['url'] = response.url
            lost["valid"] = 1
            # yield lost
