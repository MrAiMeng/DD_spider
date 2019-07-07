# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import  RedisCrawlSpider
import urllib.parse
from copy import deepcopy
# 分布式断点爬虫

class DdSpider(RedisCrawlSpider):
    name = 'dd'
    redis_key = 'dd'
    allowed_domains = ['dangdang.com']

    # start_urls = ['http://book.dangdang.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class = "con '
                                            'flq_body"]/div/dl/dd')),follow = True, ),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class = "list"]/li')), follow=True, ),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class = "list"]/li')), follow=True, ),
        # restrict_xpath 后面应该跟包含url地址的标签，而不应该将url地址取出来
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="list_aa "]/li/a')),
        callback = 'parse_item',),
        Rule(LinkExtractor(restrict_xpaths=('//a[text() = "下一页"]')), follow=True,),
    )

    def parse_item(self, response):
        item = {}
        item['book_title'] = response.xpath('//div['
                                            '@class="sale_box_left"]/div['
                                              '1]/h1/@title').extract_first()
        item['book_img'] = response.xpath('//div['
                                            '@class="pic"]/a/img/@src').extract_first()
        item['book_price'] = response.xpath('//p['
                                          '@id="dd-price"]/text()').extract()
        # 文本前有空白字符，需用extract，然后再去除空白字符
        item['book_price'] = ''.join(item['book_price']).split()
        item['author'] = response.xpath('//div['
                                            '@class="messbox_info"]/span[1]/a/text('
                                        ')').extract()
        item['press'] = response.xpath('//div['
                                            '@class="messbox_info"]/span[2]/a/text('
                                       ')').extract_first()
        # split切除空白字符
        item['publish_date'] = response.xpath('//div['
                                       '@class="messbox_info"]/span[3]/text('
                                       ')').extract_first().split()
        # content = [item1, item2, item3, item4, item5, item6, item7]
        yield(item)


