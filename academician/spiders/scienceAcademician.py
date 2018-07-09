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
        # headers = {
        #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #                  'Chrome/67.0.3396.99 Safari/537.36',
        #     'Cookie':'HttpOnly=true; Secure; Hm_lvt_141d1d902a441a529f2409bd8abe53ef=1531100639; HttpOnly=true; '
        #              'Secure; JSESSIONID=308D69AA1AF856D9F769ADF79D51DEAB; Hm_lpvt_141d1d902a441a529f2409bd8abe53ef=1531113885',
        #     'Referer':'http://www.casad.cas.cn/chnl/371/index.html'
        # }
        for academician_line in academician_lines:
            academicians = academician_line.css('span')
            for academician in academicians:
                item = AcademicianItem()
                item['name'] = academician.css('a::text').extract()[0]
                item['link'] = academician.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=item['link'],callback=self.more_parse,dont_filter=True,meta={'item':item})

    def more_parse(self,response):
        item = response.meta['item']

        # introduce = response.css('p:nth-child(1)::text').extract_first()
        introduce = response.xpath('//p[1]/text()').extract_first()
        item['dicipline'] = re.findall('.*?(?=学家)|(?=专家)',introduce)[0].strip()
        item['evaluate_time'] = re.findall('\d{4}(?=年当选)',introduce)[0].strip()
        yield item


