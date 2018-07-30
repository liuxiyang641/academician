# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcademicianItem(scrapy.Item):
    # define the fields for your item here like:
    table = 'academician'  # 导入的数据库表名
    name = scrapy.Field()  # 中科院院士姓名
    department=scrapy.Field()  # 中科院院士学部
    link = scrapy.Field()  # 院士在官网链接
    introduce = scrapy.Field()  # 院士简介
    evaluate_time = scrapy.Field()  # 当选时间


class EngineerItem(scrapy.Item):
    table = 'engineer'  # 导入的数据库表名
    name = scrapy.Field()  # 中国工程院院士
    department = scrapy.Field()  # 工程院院士学部
    link = scrapy.Field()  # 院士在官网链接
    introduce = scrapy.Field()  # 院士简介
    evaluate_time = scrapy.Field()  # 当选时间
