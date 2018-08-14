import requests
import re
import json
import os
import pymysql
from lxml import etree
from jsonpath import jsonpath



#拿取jsn信息
def sohuSpider(url):
    response=requests.get(url=url)
    content=response.content.decode('utf-8')
    html = etree.HTML(content)
    info=html.xpath('//script/text()')[4]
    info="".join(info.split())
    info=re.findall(r'highProjects\|focus":\[(.*?)\]',info)

    # print(info)
    return info


def josnFormat(info):
    infos=str('[' + info[0] + ']')
    infos=json.loads(infos)
    # print('----',infos)
    return infos


def infoList(info,d):
        # print('http://www.sohu.com'+info['path'])
        d['title'] = info['title']
        #二级页面
        d['url']=info['url']
        response = requests.get(url=info['url'])
        content_detail=response.content
        folder_path = "./" + "详细页面" + "/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        detail_name = str(info['title']) + '.html'
        filename = '%s%s' % (folder_path, detail_name)
        with open(filename, 'wb') as f:
            f.write(content_detail)
        d['html']=detail_name
        #图片
        resp_img = requests.get(url=info['cover'])
        content_img = resp_img.content
        folder_path = "./" + "image" + "/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        img_name = str(info['title']) + '.jpg'
        filename = '%s%s' % (folder_path, img_name)
        with open(filename, 'wb') as f:
            f.write(content_img)
        d['img']=img_name

        print(d)
        return d
def insertData(infos,d):
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='root', db='jh_project01', charset='utf8')

    cur = conn.cursor()
    sqlc = '''
                        create table kr(
                        id int primary key auto_increment,
                        title varchar(60),
                        img varchar(60),
                        url varchar(60),
                        html varchar(60))DEFAULT CHARSET=utf8;
                        '''
    try:
        cur.execute(sqlc)
        conn.commit()
        print("成功")
    except:
        print("错误")

    for info in infos:
        print('----',info['hidden_title'])
        if info['hidden_title'] == '1':
            continue
        else:
            d = infoList(info,d)
            sqla = '''
                        insert into kr(title,img,url,html)
                        values(%s,%s,%s,%s);
                       '''
            try:
                cur.execute(sqla, (d['title'], d['img'],d['url'], d['html']))
                conn.commit()
                print("成功")
            except:
                print("失败")

    conn.commit()
    cur.close()
    conn.close()



def main():
    d={}
    url = 'http://36kr.com/'
    info=sohuSpider(url)
    infos=josnFormat(info)
    insertData(infos,d)


main()