# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcademicianItem(scrapy.Item):
    # define the fields for your item here like:
    table='academician'
    name = scrapy.Field() # 中科院院士姓名
    link = scrapy.Field() #院士在官网链接
    dicipline = scrapy.Field() # 院士学科
    evaluate_time = scrapy.Field() # 当选时间
