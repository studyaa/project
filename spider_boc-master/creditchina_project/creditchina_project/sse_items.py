# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def delete_space(value):
    '''
    删除字符串中的所有空格
    :param value:
    :return:
    '''
    return str(value).replace(' ', '').strip()


def delete_plus(value):
    '''
    删除字符串中的"+"
    :param value:
    :return:
    '''
    return str(value).replace('+', '').strip()


def date_parse(value):
    '''
    转换为日期类型
    :param value:
    :return:
    '''
    try:
        value = value.replace('·', '').replace('/', '').strip()
        value = datetime.datetime.strptime(value, '%Y%m%d').date()
    except Exception as e:
        value = datetime.datetime.now().date()
    return str(value)


def return_value(value):
    '''
    保持原来的数值不变
    :param value:
    :return:
    '''
    return str(value).strip()


def get_value(value):
    '''
    通过正则表达式获取特定值
    :param value:
    :return:
    '''
    value = str(value).strip()
    obj = re.match('.*\[(.*?)\].*', value)
    if obj:
        return obj.group(1)
    else:
        return value
class SseLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()

class SseResultItem(scrapy.Item):
    batch_date = scrapy.Field()
    security_code = scrapy.Field()
    security_nick = scrapy.Field()
    pub_date = scrapy.Field()
    writ_no = scrapy.Field()
    party_name = scrapy.Field()
    pub_type = scrapy.Field()
    table_name = scrapy.Field()