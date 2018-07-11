# -*- coding: utf-8 -*-
import scrapy

from academician.items import AcademicianItem

import re


class ScienceacademicianSpider(scrapy.Spider):
    name = 'scienceAcademician'
    allowed_domains = ['http://www.casad.cas.cn']
    start_urls = ['http://www.casad.cas.cn/chnl/371/index.html']

    def parse(self, response):
        academician_lines = response.css('#allNameBar dd')
        for academician_line in academician_lines:
            academicians = academician_line.css('span')
            for academician in academicians:
                item = AcademicianItem()
                item['name'] = academician.css('a::text').extract()[0]
                item['link'] = academician.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=item['link'],callback=self.more_parse,dont_filter=True,meta={'item':item})

    def more_parse(self,response):
        item = response.meta['item']
        # if(response.xpath('//p')):
        #     if(response.xpath('//p[1]/text()')):
        #         introduce = response.xpath('//p[1]/text()').extract_first()
        #     elif(response.xpath('//p[1]/span/text()')):
        #         introduce = response.xpath('//p[1]/span/text()').extract_first()
        #     else:
        #         introduce = response.xpath('//p[1]/font/text()').extract_first()
        # else:
        #     introduce = response.xpath('//*[@id="zoom"]/text()').extract_first()
        introduce_select = response.xpath('//*[@id="zoom"]//text()')
        introduce = ''
        introduces = [intro.extract() for intro in introduce_select]
        for intro in introduces:
            introduce += intro

        item['introduce'] = introduce.strip()

        # if(re.findall('.*?[家学]', introduce)):
        #     item['dicipline'] = re.findall('.*?[家学]', introduce)[0].strip()
        # else:
        #     item['dicipline'] = '未知'

        if(re.findall('\d{4}(?=年当选)',introduce)):
            item['evaluate_time'] = re.findall('\d{4}(?=年当选)',introduce)[0].strip()
        else:
            item['evaluate_time'] = '未知'

        yield item


