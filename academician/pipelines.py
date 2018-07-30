# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class AcademicianPipeline(object):
#     def process_item(self, item, spider):
#         return item


from scrapy.exceptions import DropItem
from academician.items import AcademicianItem, EngineerItem
import csv

class DuplicatePipeline(object):
    """
    去除重复item
    请对spider.name进行判断
    """

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if spider.name == "engineer":
            if item['link'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['link'])
                return item
        else:
            return item


class CsvExporterPipeline(object):
    """
    导出到csv
    """

    def open_spider(self, spider):
        if spider.name == "engineer":   # 工程院院士
            self.file = open('../docs/AcademicianEngineering.csv', 'w', encoding='utf-8-sig')
            header = []
            for key in EngineerItem.fields:
                header.append(key)
        else:   # 科学院院士
            self.file = open('../docs/AcademicianScience.csv', 'w', encoding='utf-8-sig')
            header = []
            for key in AcademicianItem.fields:
                header.append(key)

        self.writer = csv.DictWriter(self.file, fieldnames=header)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        self.file.flush()
        return item





# import pymysql

# class MysqlPipeline():
#
#     def __init__(self,host,database,user,password,port):
#         self.host = host
#         self.database = database
#         self.user = user
#         self.password = password
#         self.port = port
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         return cls(
#             host=crawler.settings.get('MYSQL_HOST'),
#             database=crawler.settings.get('MYSQL_DATABASE'),
#             user=crawler.settings.get('MYSQL_USER'),
#             password=crawler.settings.get('MYSQL_PASSWORD'),
#             port=crawler.settings.get('MYSQL_PORT')
#         )
#
#     def open_spider(self,spider):
#         self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
#         self.cursor = self.db.cursor()
#
#     def close_spider(self,spider):
#         self.db.close()
#
#     def process_item(self,item,spider):
#         data = dict(item)
#         keys = ', '.join(data.keys())
#         values = ', '.join(['%s']*len(data))
#         sql = 'INSERT INTO %s(%s) VALUES(%s)'%(item.table,keys,values)
#         self.cursor.execute(sql,tuple(data.values()))
#         self.db.commit()
#         return item
