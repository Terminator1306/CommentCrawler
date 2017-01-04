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
        # for item in items_list:
        item = items_list[0]
        yield scrapy.Request(
                url=self.main_url + item,
                dont_filter=True,
                callback=self.nameparse
            )
        # if len(next_page) > 0:
        #     yield scrapy.Request(
        #         url=self.main_url + next_page
        #     )

    def nameparse(self, response):
        sel = scrapy.Selector(response)
        detail = sel.xpath("//script[@type='text/javascript']").extract()[6]
        detail = re.sub('[\\s]', '', detail)
        brand = re.sub(".*manuName=\\'(.*?)\\';.*", '\\1', detail)
        product_id = 'ZOL'+re.sub(".*proId=\\'(.*?)\\';.*", '\\1', detail)
        model = sel.xpath("//div[@class='breadcrumb']/span/text()").extract()[0]
        name = sel.xpath("//div[@class='page-title clearfix']/h1/text()").extract()[0]
        price = sel.xpath("//span[@id='J_PriceTrend']/b[@class='price-type price-retain']/text()").extract()[0]
        comment_count = sel.xpath("//div[@class='total-num']/span/text()").extract()[0][:-3]
        para_url = sel.xpath("//div[@class='section-header']/a/@href").extract()[0]
        yield scrapy.Request(
            url=self.main_url+para_url,
            dont_filter=True,
            callback=self.paraparse,
            meta={"brand": brand, "model": model, "product_id": product_id,
                  "name": name, "price": price, "comment_count":comment_count}
        )

    def paraparse(self, response):
        sel = scrapy.Selector(response)
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
        product['product_id'] = response.meta['product_id']
        product['brand'] = response.meta['brand']
        product['model'] = response.meta['model']
        product['name'] = response.meta['name']
        product['price'] = response.meta['price']
        product['attribute'] = attributes
        # yield product

