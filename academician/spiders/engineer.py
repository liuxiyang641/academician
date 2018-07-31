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
        # 所有学部
        bts = response.css('.ysmd_bt::text')
        nums_of_bts = len(bts)
        index = 0
        while index < nums_of_bts:
            name_list = response.xpath(
                '//div[@class="ysxx_namelist clearfix" and count(preceding-sibling::div[@class="ysmd_bt clearfix"])=' + str(index + 1) + ']')
            engineers = name_list.css('li[class="name_list"]')
            for engineer in engineers:
                item = EngineerItem()
                name = engineer.css('a::text').extract_first()
                item['XB'] = re.findall('.*、(.*)\((.*)', bts[index].extract())[0][0]
                item['name'] = re.findall('[\u4e00-\u9fa5]{2,4}', name)[0]
                item['link'] = base_url + engineer.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=item['link'], callback=self.more_parse, dont_filter=True, meta={'item': item})
            index += 1

    def more_parse(self, response):
        item = response.meta['item']
        if (response.xpath('//div[@class="intro"]//p/text()')):
            introduce_select = response.xpath('//div[@class="intro"]//p/text()')
            introduce = ''
            introduces = [intro.extract() for intro in introduce_select]
            for intro in introduces:
                introduce += intro
            item['introduce'] = introduce

            if (re.findall('\d{4}(?=年当选为中国工程院院士)', introduce)):
                item['evaluate_time'] = re.findall('\d{4}(?=年当选为中国工程院院士)', introduce)[0].strip()
            else:
                item['evaluate_time'] = 1901
        else:
            item['introduce'] = None
            item['evaluate_time'] = 1901
        yield item
