import requests
import os
import pymysql
from lxml import etree

headers={
'Host':'tech.qq.com',
'Connection':'keep-alive',
'Cache-Control':'max-age=0',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9'
}

def getInfoList(url):
    response=requests.get(url=url)
    content=response.content
    content=content.decode('gbk')
    with open('./baidu.html','w') as f:
        f.write(content)
    html=etree.HTML(content)
    info_list=html.xpath('//div[@class="m-list"]/ul[@class="f-cb"]/li')
    print(info_list)
    return info_list

def fillList(info,infos):
    infos['title']=info.xpath('./a/text()')[0]
    infos['url']=info.xpath('./a/@href')[0]
    # 保存详情页面
    resp_detail = requests.get(url=infos['url'])
    content_detail = resp_detail.content
    folder_path = "./" + "详细页面" + "/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    detail_name = str(infos['title']) + '.html'
    filename = '%s%s' % (folder_path, detail_name)
    with open(filename, 'wb') as f:
        f.write(content_detail)
    infos['html']=detail_name

    print(infos)
    return infos

def printInfo(infos,info_list):
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='root', db='jh_project01', charset='utf8')

    cur = conn.cursor()
    sqlc = '''
                    create table ir(
                    id int primary key auto_increment,
                    title varchar(60),
                    url varchar(100),
                    html varchar(60))DEFAULT CHARSET=utf8;
                    '''
    try:
        cur.execute(sqlc)
        conn.commit()
        print("成功")
    except:
        print("错误")

    for info in info_list:
        infos = fillList(info, infos)
        sqla = '''
                insert into ir(title,url,html)
                values(%s,%s,%s);
               '''
        try:
            cur.execute(sqla, (infos['title'], infos['url'],infos['html']))
            conn.commit()
            print("成功")
        except:
            print("失败")

    conn.commit()
    cur.close()
    conn.close()

def main():
    infos = {}
    url =  'http://www.iresearch.cn/'
    info_list = getInfoList(url)
    printInfo(infos,info_list)


main()