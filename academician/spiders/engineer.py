# -*- coding: utf-8 -*-
import scrapy

from academician.items import EngineerItem

import re


class EngineerSpider(scrapy.Spider):
    name = 'engineer'
    allowed_domains = ['http://www.cae.cn']
    start_urls = ['http://www.cae.cn/cae/html/main/col48/column_48_1.html/']

    def parse(self, response):
        base_url = 'http://www.cae.cn'
        engineers = response.css('li[class="name_list"]')
        for engineer in engineers:
            item = EngineerItem()
            item['name'] = engineer.css('a::text').extract_first()
            item['link'] = base_url+engineer.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=item['link'],callback=self.more_parse,dont_filter=True,meta={'item':item})

    def more_parse(self,response):
        item = response.meta['item']
        introduce_select = response.xpath('//div[@class="intro"]//p/text()')
        introduce=''
        introduces = [intro.extract() for intro in introduce_select]
        for intro in introduces:
            introduce+=intro

        # if(re.findall('(?<=。).*?专家',introduce)):
        #     item['dicipline'] = re.findall('(?<=。).*?专家',introduce)[0].strip()
        # else:
        #     item['dicipline'] = '未知'
        item['introduce'] = introduce
        # introduce2 = response.xpath('//div[@class="intro"]/p[last()]/text()').extract_first()
        if(re.findall('\d{4}(?=年当选为中国工程院院士)',introduce)):
            item['evaluate_time'] = re.findall('\d{4}(?=年当选为中国工程院院士)',introduce)[0].strip()
        else:
            item['evaluate_time'] = '未知'
        yield item
