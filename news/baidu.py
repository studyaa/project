import requests
import os
import pymysql
from lxml import etree


def getInfoList(url):
    response=requests.get(url=url)
    content=response.content
    content=content.decode('gbk')
    # with open('./baidu.html','w') as f:
    #     f.write(content)
    html=etree.HTML(content)
    info_list=html.xpath('//ul[@class="ulist fb-list"]')[0]
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
                    create table baidu(
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
                insert into baidu(title,url,html)
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
    url =  'http://tech.baidu.com/'
    info_list = getInfoList(url)
    # for info in info_list:
    #     infos = fillList(info, infos)
    printInfo(infos,info_list)


main()