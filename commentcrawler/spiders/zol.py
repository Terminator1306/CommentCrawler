import scrapy
import re
from commentcrawler.items import *
import json
import HTMLParser


class ZolSpider(scrapy.Spider):
    name = "zol"
    main_url = "http://detail.zol.com.cn"
    allowed_domains = ["zol.com.cn"]
    start_urls = [
        "http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html"
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        items_list = sel.xpath('//li[@data-follow-id]/a/@href').extract()
        next_page = sel.xpath('//a[@class="next"]/@href').extract()
        for item in items_list:
        # item = items_list[0]
            yield scrapy.Request(
                    url=self.main_url + item,
                    dont_filter=True,
                    callback=self.nameparse
                )
        if len(next_page) > 0:
            yield scrapy.Request(
                url=self.main_url + next_page[0],
                dont_filter=True,
                callback=self.parse
            )

    def nameparse(self, response):
        sel = scrapy.Selector(response)
        detail = sel.xpath("//script[@type='text/javascript']").extract()[6]
        detail = re.sub('[\\s]', '', detail)
        brand = re.sub(".*manuName=\\'(.*?)\\';.*", '\\1', detail)
        product_id = re.sub(".*proId=\\'(.*?)\\';.*", '\\1', detail)
        model = sel.xpath("//div[@class='breadcrumb']/span/text()").extract()[0]
        name = sel.xpath("//div[@class='page-title clearfix']/h1/text()").extract()[0]
        price = sel.xpath("//span[@id='J_PriceTrend']/b[@class='price-type price-retain']/text()").extract()
        if len(price) > 0:
            price = price[0]
        else:
            price = 'null'
        comment_count = sel.xpath("//div[@class='total-num']/span/text()").extract()[0][:-3]
        para_url = sel.xpath("//div[@class='section-header']/a/@href").extract()[0]
        # get product's parameter
        yield scrapy.Request(
            url=self.main_url+para_url,
            dont_filter=True,
            callback=self.paraparse,
            meta={"brand": brand, "model": model, "product_id": product_id,
                  "name": name, "price": price, "comment_count":comment_count}
        )
        # get product's comment
        for page in range(1, int(comment_count)/10 + 2):
            yield scrapy.Request(
                url="http://detail.zol.com.cn/xhr3_Review_GetListAndPage_isFilter=0%5EproId="+product_id+"%5Epage="+str(page)+".html",
                meta={"brand": brand, "model": model, "product_id": product_id,
                      "name": name, "price": price, "comment_count":comment_count},
                callback=self.commentparse
            )

    def paraparse(self, response):
        sel = scrapy.Selector(response)
        viewpage = sel.xpath("//a[@class='ol-comment']/@href").extract()[0]
        tables = sel.xpath("//div[@class='param-table']/table")
        attributes = {}
        for table in tables:
            table_header = table.xpath('./tr/th/text()').extract()[0]
            para_dict = {}
            for row in table.xpath('./tr//ul[@class="category-param-list"]/li'):
                data = row.xpath("./span//text()").extract()
                para_dict[data[0]] = data[1]
            attributes[table_header] = para_dict
        product = Product()
        product['comment_count'] = response.meta['comment_count']
        product['category'] = 'phone'
        product['item_type'] = 'product'
        product['product_id'] = "ZOL"+response.meta['product_id']
        product['brand'] = response.meta['brand']
        product['model'] = response.meta['model']
        product['name'] = response.meta['name']
        product['price'] = response.meta['price']
        product['attribute'] = attributes
        product['commentTag'] = ''
        yield scrapy.Request(
            url=self.main_url+viewpage,
            meta={"product": product},
            callback=self.commenttagparse
        )

    def commenttagparse(self, response):
        sel = scrapy.Selector(response)
        word_list = sel.xpath("//ul[@class='words-list clearfix']/li/a/@title").extract()
        response.meta['product']['commentTag'] = word_list
        yield response.meta['product']

    def commentparse(self, response):
        sel = scrapy.Selector(response)
        comment_set = sel.xpath("//li[starts-with(@class, '\\\"comment-item')]")
        for item in comment_set:
            good = item.xpath(".//strong[@class='\\\"good\\\"']/p/span/text()").extract()
            good = "".join(good).decode('string_escape')
            good.replace('\\n', '')
            if len(good) != 0:
                good_comment = zol_Comment()
                good_comment['item_type'] = 'zol_comment'
                good_comment['content'] = good.decode('unicode-escape')
                good_comment['orientation'] = 1
                good_comment['product_id'] = response.meta['product_id']
                yield good_comment

            bad = item.xpath(".//strong[@class='\\\"bad\\\"']/p/span/text()").extract()
            bad = "".join(bad).decode('string_escape')
            bad.replace('\\n', '')
            if len(bad) != 0:
                bad_comment = zol_Comment()
                bad_comment['product_id'] = response.meta['product_id']
                bad_comment['content'] = bad.decode('unicode-escape')
                bad_comment['orientation'] = -1
                bad_comment['item_type'] = 'zol_comment'
                yield bad_comment

            summary = item.xpath(".//strong[@class='\\\"summary\\\"']/p/span/text()").extract()
            summary = "".join(summary).decode('string_escape')
            summary.replace('\\n', '')
            if len(summary) != 0:
                summary_comment = zol_Comment()
                summary_comment['item_type'] = 'zol_comment'
                summary_comment['content'] = summary.decode('unicode-escape')
                summary_comment['orientation'] = 0
                summary_comment['product_id'] = response.meta['product_id']
                yield summary_comment
