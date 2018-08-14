# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqsiqResultItem(scrapy.Item):
    table = 'AQSIQ'
    batch_date = scrapy.Field()
    comp_name = scrapy.Field()
    place = scrapy.Field()
    product_name = scrapy.Field()
    spec_type = scrapy.Field()
    produce_date = scrapy.Field()
    desq_pro = scrapy.Field()
    insp_agency = scrapy.Field()
    release_date = scrapy.Field()

class BxjgResultItem(scrapy.Item):
    table = 'BXJG'
    batch_date = scrapy.Field()
    comp_name = scrapy.Field()
    abode = scrapy.Field()
    repres = scrapy.Field()
    mine_name = scrapy.Field()
    id_number = scrapy.Field()
    duty = scrapy.Field()
    refer_num = scrapy.Field()
    reles_date = scrapy.Field()
    pun_con = scrapy.Field()

class BxjgResultBureauItem(scrapy.Item):
    table = 'BXJG_BUREAU'
    batch_date = scrapy.Field()
    comp_name = scrapy.Field()
    abode = scrapy.Field()
    repres = scrapy.Field()
    mine_name = scrapy.Field()
    id_number = scrapy.Field()
    duty = scrapy.Field()
    refer_num = scrapy.Field()
    reles_date = scrapy.Field()
    pun_con = scrapy.Field()

class TudiResultItem(scrapy.Item):
    table = 'TUDI'
    totalUrl=scrapy.Field()
    ordnum=scrapy.Field()
    country = scrapy.Field()
    num = scrapy.Field()
    myname = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    myuse = scrapy.Field()
    way = scrapy.Field()
    price = scrapy.Field()
    person = scrapy.Field()
    start = scrapy.Field()
    finish = scrapy.Field()
    compact = scrapy.Field()