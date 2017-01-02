#coding:utf-8
import scrapy
import re
from commentcrawler.items import *
import json
import HTMLParser


class TmallSpider(scrapy.Spider):
    name = "Tmall"
    allowed_domains = ["tmall.com"]
    start_urls = {
        'phone':"https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.muAm62&cat=50024400&q=%CA%D6%BB%FA&sort=s&style=g&search_condition=7&from=sn_1_rightnav&industryCatId=50024400#J_crumbs",
        # 'laptop':"https://list.tmall.com/search_product.htm?spm=875.7931836/A.subpannel2016040.22.RAIxE6&cat=50024399&acm=2016031437.1003.2.720502&aldid=0XR95i8Y&theme=663&scm=1003.2.2016031437.OTHER_1458241115467_720502&pos=1",
        # 'refrigerator':"https://list.tmall.com/search_product.htm?spm=a222t.7794920.fsnav.1.mpZFxJ&cat=50918004&acm=lb-zebra-24139-328537.1003.8.455785&scm=1003.8.lb-zebra-24139-328537.ITEM_14458832193540_455785",
        # 'novel':'https://list.tmall.com/search_product.htm?spm=a223b.7742558.8309007222.12.W59Byp&cat=50021926&sort=s&acm=lb-zebra-7852-323689.1003.8.450706&style=g&from=sn_1_cat&scm=1003.8.lb-zebra-7852-323689.ITEM_14432252898171_450706&tmhkmain=0#J_crumbs',
        # 'm_clothes':"https://list.tmall.com/search_product.htm?spm=a221t.1710963.8073444875.12.vdFreu&cat=50074112&shopType=any&sort=s&style=g&acm=lb-zebra-7499-292762.1003.8.427962&search_condition=23&promo=43906&industryCatId=50026245&active=1&from=sn_1_rightnav&scm=1003.8.lb-zebra-7499-292762.ITEM_14417598541394_427962",
        # 'purse':"https://list.tmall.com/search_product.htm?spm=875.7931836/A.subpannel2016031.45.PU2DBq&abbucket=&cat=55752015&sort=s&acm=201603102.1003.2.718817&aldid=4zud7MVQ&from=sn_1_cat&pos=3&style=g&search_condition=23&industryCatId=55722012&abtest=&scm=1003.2.201603102.OTHER_1465575214063_718817&tmhkmain=0#J_crumbs",
        # 'snacks':"https://list.tmall.com/search_product.htm?spm=875.7931836/A.subpannel2016046.14.PU2DBq&acm=2016030721.1003.64.709543&q=%C1%E3%CA%B3&vmarket=&aldid=oWkQTa94&from=mallfp..pc_1_searchbutton&type=p&scm=1003.64.2016030721.OTHER_1456794819190_709543&pos=1",
        # 'm_shoes':"https://list.tmall.com/search_product.htm?spm=875.7931836/A.subpannel2016031.27.PU2DBq&cat=53406005&sort=s&style=g&acm=201603076.1003.2.708919&search_condition=7&aldid=4zud7MVQ&theme=713&industryCatId=50076895&active=1&from=sn_1_cat&smAreaId=330100&scm=1003.2.201603076.OTHER_1467379424209_708919&pos=1",
        # 'w_shoes':"https://list.tmall.com/search_product.htm?spm=875.7931836/A.subpannel2016031.11.PU2DBq&new=1&cat=50036330&acm=201603075.1003.2.708912&search_condition=71&aldid=4zud7MVQ&theme=714&scm=1003.2.201603075.OTHER_1467006793803_708912&pos=1",
        # 'w_clothes':"https://list.tmall.com/search_product.htm?spm=875.7931836/A.subpannel2016025.2.PU2DBq&cat=50025135&sort=s&style=g&acm=2016031463.1003.2.718839&aldid=4bLwqBrw&oq=%C5%AE%D7%B0&prop=122216347:854168429&from=sn_1_prop&scm=1003.2.2016031463.OTHER_1471742023942_718839&tmhkmain=0&pos=2#J_crumbs"
    }
    cookies = {
                'cna':'MgGQDlZ+nHsCAWonKbYoFjaM',
                '_med':'dw:1440&dh:900&pw:1440&ph:900&ist:0',
                't':'265651046d436fb6c5a7a398e4d65a4c',
                '_tb_token_':'oIA8dqMGpOuU',
                'cookie2':'1abd1988561b207bbffbc860ebcbeb2f',
                'pnm_cku822':'075UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktwRX5FeEF5THNNciQ%3D%7CU2xMHDJ7G2AHYg8hAS8WIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGdSaVJvVm5bZFplUm9NdEl3SXdPc0l9RXhEcUR9R2k%2F%7CVWldfS0TMwY4BycSMhwkFHMIWDVfe1UDVQ%3D%3D%7CVmhIGCUFOQc8BycbIh0jAzgFPAIiHiceIwM3CjcXKxIrFjYDOAVTBQ%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
                'res':'scroll%3A1423*6043-client%3A1423*799-offset%3A1423*6043-screen%3A1440*900',
                'cq':'ccp%3D1',
                'l':'AoCAedPj4WQcxKerV6ErAiSI0ARSCWTT',
                'isg':'AikpBI00WtENd2aQhdgdXB8vONXKrB0oyAa8HMsepZBPkkmkE0Yt-BeAIoFe'
        }

    def start_requests(self):
        for k,v in self.start_urls.iteritems():
            yield scrapy.Request(v,cookies=self.cookies,callback=self.parse,meta={'cat':k})
    

    def parse(self, response):
        sel = scrapy.Selector(response)
        items = sel.xpath('//div[@class="product  "]')
        next_page = sel.xpath('//a[@class="ui-page-next"]/@href').extract()
        # print len(items)
        for item in items:
            # item = items[0]
            product_id = "TM_"+item.xpath("@data-id").extract()[0]
            url = "https:"+item.xpath(".//div[@class='productImg-wrap']/a/@href").extract()[0]
            price = item.xpath(".//p[@class='productPrice']/em/@title").extract()[0]
            yield scrapy.Request(
                url="https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s"%(product_id[3:],),
                meta={'price':price,'product_id':product_id,'url':url,'cat':response.meta['cat']},
                cookies=self.cookies,
                callback=self.CommentCountParse
                )
        if len(next_page)>0:
            yield scrapy.Request(
                url="https://list.tmall.com/search_product.htm"+next_page[0],
                callback = self.parse,
                cookies = self.cookies,
                meta = {'cat':response.meta['cat']}
                )


    def CommentCountParse(self,response):
        sel = scrapy.Selector(response)
        body = sel.xpath("//body//text()").extract()[0]
        mjson = json.loads(body[9:-1])
        yield scrapy.Request(
            url="https://rate.tmall.com/listTagClouds.htm?itemId=%s"%(response.meta['product_id'][3:],),
            meta={'price':response.meta['price'],'product_id':response.meta['product_id'],'url':response.meta['url'],
                'gradeAvg':mjson['dsr']['gradeAvg'],'comment_count':mjson['dsr']['rateTotal'],'cat':response.meta['cat']},
            cookies=self.cookies,
            callback=self.CommentTagParse
            )


    def CommentTagParse(self,response):
        sel = scrapy.Selector(response)
        body = '{' + sel.xpath("//body//text()").extract()[0] + "}"
        # with open("result.txt",'w') as f:
        #     f.write(body)
        mjson = json.loads(body)
        commentTag = {}
        for tag in mjson['tags']['tagClouds']:
            commentTag[tag['tag']] = tag['count']
        yield scrapy.Request(
            url=response.meta['url'],
            meta={'price':response.meta['price'],'product_id':response.meta['product_id'],'commentTag':commentTag,
                'gradeAvg':response.meta['gradeAvg'],'comment_count':response.meta['comment_count'],'cat':response.meta['cat']},
            cookies=self.cookies,
            callback=self.ProductParse
            )


    def ProductParse(self,response):
        sel = scrapy.Selector(response)
        body = sel.xpath("//body").extract()[0]
        detail = sel.xpath("//div[@id='J_Attrs']/table[1]/tbody")
        product_id = response.meta["product_id"]
        attribute = {'gradeAvg':response.meta['gradeAvg']}
        info = re.sub("[\\n ]","",sel.xpath("//div[@class='tm-clear']/script").extract()[-1])
        model = ""
        brand = re.sub(".*\"brand\":\"(.*?)\"[,\\}].*",'\\1',info)
        html_parser = HTMLParser.HTMLParser()
        brand = html_parser.unescape(brand)
        if len(brand)>100:
            brand = ""
        # with open("brand.txt","a") as f:
        #     f.write(brand+"\n")
        name = sel.xpath("//meta[@name='keywords']/@content").extract()[0]
        if len(detail)>0:
            keys = detail.xpath("./tr[not(@class)]/th/text()").extract()
            values = detail.xpath("./tr[not(@class)]/td/text()").extract()
            for index,key in enumerate(keys):
                attribute[key] = values[index]
                if re.compile(u".*型号").match(key):
                    model = values[index]
        product = Product()
        product['comment_count'] = response.meta['comment_count']
        product['item_type'] = "product"
        product['price'] = response.meta["price"]
        product['name'] = name
        product['product_id'] = product_id
        product['brand'] = brand
        product['model'] = model
        product['attribute'] = attribute
        product['commentTag'] = response.meta['commentTag']
        product['category'] = response.meta['cat']
        yield product

        limit = 99
        pages = int(response.meta['comment_count'])/20+1 
        if pages > limit:
            pages = limit
        for i in range(1,pages):
            yield scrapy.Request(
            url="https://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=1&order=3&currentPage=%d"%(product_id[3:],i),
            meta={'product_id':response.meta['product_id'],'page':i},
            cookies=self.cookies,
            callback=self.CommentParse
            )


    def CommentParse(self,response):
        sel = scrapy.Selector(response)
        body = sel.xpath("//body//text()").extract()[0]
        mstr = "{" + body + "}"
        try :
            mjson = json.loads(mstr)
            for rate in mjson["rateDetail"]["rateList"]:
                comment = Comment()
                comment['attribute']={}
                comment['product_id'] = response.meta['product_id']
                comment['comment_id'] = rate['id']
                comment['creationTime'] = rate['rateDate']
                comment['content'] = rate['rateContent']
                comment['item_type'] = 'comment'
                comment['referenceName'] = rate['auctionSku']
                if len(rate['pics'])>0:
                    comment['attribute']['pics'] = True
                comment['attribute']['appendComment'] = rate['appendComment']
                comment['attribute']['userlevel'] = rate['tamllSweetLevel']
                if rate['attributesMap'] != '' and rate['attributesMap'].containsKey('worth_score'):
                    comment['attribute']['worth_score'] = rate['attributesMap']['worth_score']
                comment['attribute']['aliMallSeller'] = rate['aliMallSeller']
                comment['attribute']['auctionPrice'] = rate['auctionPrice']
                yield comment
        except Exception,e:
            print str(e)
            lost = Lost()
            lost['item_type'] = 'lost'
            lost['url'] = response.url
            lost['content'] = str(e)
            lost['page'] = response.meta['page']
            lost['product_id'] = response.meta['product_id']
            lost['valid'] = 1
            # yield lost
