#-*- coding:utf-8 -*-
import requests
from lxml import etree
import random
import datetime
import time
import re
from bloom_filter import BloomFilter
from pymongo import MongoClient

client = MongoClient('mongodb://laocheng:laocheng@192.168.0.11:27017')

# 数据库名称
db=client.DaZhdp
# 表名称
dzdp=db.dzdp
proxy_ip = ""
shop_list=[]
def get_proxy_ip(regenerate):
    global proxy_ip
    if regenerate or proxy_ip == "":
        while True:
            try:
                proxy_ip_res=requests.get(url='http://api.ip.data5u.com/dynamic/get.html?order=3ad7917c16dc90af3b87941f5e9c173b&ttl=1&random=true&sep=3').content
                proxy_ip = str(proxy_ip_res).split(",")[0].strip("b'")
                # print("new proxy_ip: " + proxy_ip)
                break
            except Exception as e:
                print(e)
    # print("return proxy_ip:" + proxy_ip)
    return proxy_ip

def crawl_dp_page(url, type):
    # print("crawl_db_page(" + type + "): " + url)
    proxy = get_proxy_ip(False)
    while True:
        try:
            response = requests.get(url=url,headers=headers,proxies={'http':'http://'+proxy})
            if response.status_code == 200:
                print(proxy)
                return response.content.decode('utf-8')
            proxy = get_proxy_ip(True)
        except Exception as e:
            print(e)

def crawl_city_page(url):
    # BLOOMF???
    bloomf = BloomFilter(10000000, 0.01)
    # print(bloomf)
    #全国城市url
    city_page_content = crawl_dp_page(url, 'citylist')
    # print(city_page_content,'>>>>>')
    html = etree.HTML(city_page_content)
    #这是全国城市链接
    city_urls = html.xpath('//div[@class="findHeight"]/a/@href')
    print(city_urls)

    for city_detail_url in city_urls:
        page = 1
        while True:
            #商铺列表页面
            city_detail_page_content = crawl_dp_page("http:"+city_detail_url+"/ch20/g187p%s"%page, 'citydetailpage')
            #商铺详情链接url
            shop_urls = re.findall(r'href="(.+/shop/[0-9]+)"', city_detail_page_content)
            tot_shop = 0
            for shop_url in shop_urls:
                if shop_url in bloomf:
                    print("ignore duplicate " + shop_url)
                else:
                    #商铺详情页
                    shop_content = crawl_dp_page(shop_url, 'shopdetail')
                    bloomf.add(shop_url)#None
                    parse_shop(shop_content)#None
                    tot_shop += 1
            if tot_shop < 1: # break if there is no shop on that page
                break
            page += 1

def parse_shop(shop_urls):
    htmls = etree.HTML(shop_urls)
    shop = {}
    try:
        shop['标题'] = htmls.xpath('//h1[@class="shop-name"]/text()')[0]
    except:
        shop['标题']=''
    try:
        shop['评论'] = htmls.xpath('//*[@id="reviewCount"]/text()')[0]
    except:
        shop['评论']=''
    try:
        shop['消费'] = htmls.xpath('//*[@id="avgPriceTitle"]/text()')[0]
    except:
        shop['消费']=''
    try:
        shop['产品'] = htmls.xpath('//*[@id="comment_score"]/span[1]/text()')[0]
    except:
        shop['产品']=''
    try:
        shop['环境'] = htmls.xpath('//*[@id="comment_score"]/span[2]/text()')[0]
    except:
        shop['环境']=''
    try:
        shop['服务'] = htmls.xpath('//*[@id="comment_score"]/span[3]/text()')[0]
    except:
        shop['服务']=''
    try:
        shop['地址'] = htmls.xpath('//span[@class="item"]/@title')[0]
    except:
        shop['地址'] = ''
    try:
        shop['星级'] = htmls.xpath('//div[@class="brief-info"]/span/@title')[0]
    except:
        shop['星级'] = ''
    try:
        shop['城市'] = htmls.xpath('//*[@id="logo-input"]/div/a[2]/span[2]/text()')[0]
    except:
        shop['城市'] = ''
    try:
        shop['类型'] = htmls.xpath('//*[@id="body"]/div/div[1]/a[2]/text()')[0]
    except:
        shop['类型'] = ''
    print(shop['标题'])
    print(shop['评论'])
    print(shop['消费'])
    print(shop['产品'])
    print(shop['环境'])
    print(shop['服务'])
    print(shop['地址'])
    print(shop['星级'])
    print(shop['城市'])
    print(shop['类型'])
    shops = dzdp.insert_one(
        {"city": shop['城市'],
         "title": shop['标题'],
         "shop": shop['类型'],
         "address": shop['地址'],
         "comment": shop['评论'],
         "consumption": shop['消费'],
         "grade": shop['星级'],
         "product": shop['产品'],
         "environment": shop['环境'],
         "serve": shop['服务'],
         "crawl_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         }).inserted_id
    shop_list.append(shop)

if __name__ == '__main__':
    headers = {

        'Host': 'www.dianping.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.dianping.com/search/keyword/160/10_a/p42',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie':'_lxsdk_cuid=1634923d6f4c8-056518689d0a1f-3b60490d-13c680-1634923d6f5c8; _lxsdk=1634923d6f4c8-056518689d0a1f-3b60490d-13c680-1634923d6f5c8; _hc.v=3386cd02-332b-39e4-e022-122d21a3b38f.1525940476; s_ViewType=10; ua=dpuser_7660178676; ctu=22e5c45566d5c74d4e94fde11c9c61b2de0e3d1f7ac0f1ec8e8a19e282dfcb08; cy=1; cye=shanghai; dper=2f0686858d94fac7dbe5016b1599e1fdb9cdc744bc2479d8b9188115d0ac47469b9d75beac67692c9dfaa3fc747e83669e829e251f722f8c3f722ab2c1f223bd583a40021028626d51572cef364399b95ad9f3171389c524a5cd2ee8e4bd794b; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16362507f3a-4bc-b45-6b8%7C%7C217',
    }

    start_time = time.time()
    url = 'https://www.anjuke.com/sy-city.html'
    crawl_city_page(url)
    end_time = time.time()
    print('%s' % (end_time - start_time))