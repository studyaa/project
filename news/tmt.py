import requests
import os
import pymysql
from lxml import etree


headers={
'Host':'www.tmtpost.com',
'Connection':'keep-alive',
'Cache-Control':'max-age=0',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9'
}


def getInfoList(url):
    response=requests.get(url=url,headers=headers)
    content=response.content.decode('utf-8')
    html=etree.HTML(content)
    info_list = html.xpath('//div[@class="part-cont"]')
    return info_list

def fillList(info,infos):
    infos['title']=info.xpath('./a/img/@alt')[0]
    print(1111,infos['title'])
    img_url=info.xpath('./a/img/@src')[0]
    #请求图片链接
    resp_img = requests.get(url=img_url)
    content_img = resp_img.content
    #创建文件夹保存图片
    folder_path = "./" + "image" + "/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    img_name = str(infos['title']) + img_url[img_url.rfind('.'):]
    filename = '%s%s' % (folder_path, img_name)
    with open(filename,'wb') as f:
        f.write(content_img)
    infos['img']=img_name

    #保存详情页面
    detail_url=info.xpath('./a/@href')[0]
    infos['url']='http://www.tmtpost.com'+detail_url
    resp_detail = requests.get(url=infos['url'])
    content_detail = resp_detail.content
    folder2_path = "./" + "详细页面" + "/"
    if not os.path.exists(folder2_path):
        os.makedirs(folder2_path)
    detail_name = str(infos['title']) + '.html'
    filename = '%s%s' % (folder2_path, detail_name)
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
                    create table tmt(
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
    for info in info_list:
        # print(111111)
        infos = fillList(info, infos)
        sqla = '''
                insert into tmt(title,img,url,html)
                values(%s,%s,%s,%s);
               '''
        try:
            cur.execute(sqla, (infos['title'],infos['img'], infos['url'],infos['html']))
            conn.commit()
            print("成功")
        except:
            print("失败")

    conn.commit()
    cur.close()
    conn.close()

def main():
    infos = {}
    url =  'http://www.tmtpost.com/'
    info_list = getInfoList(url)
    printInfo(infos,info_list)

main()