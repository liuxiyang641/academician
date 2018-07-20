# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 7:18 PM
# @Author  : liuxiyang

from scrapy import cmdline

name = 'engineer'
# name='scienceAcademician'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())