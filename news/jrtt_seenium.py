import requests
import os
import pymysql
from selenium import webdriver

def getHeaders():
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
    }
    return headers

def fillList(infos,i):
    infos['title']=i.find_element_by_xpath('./div/div[1]/div/div/a').text
    infos['url']=i.find_element_by_xpath('./div/div[1]/div/div/a').get_attribute("href")
    #保存二级页面
    resp_detail = requests.get(url=infos['url'],headers=getHeaders())
    content_detail = resp_detail.content
    folder_path = "./" + "详细页面" + "/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    detail_name = str(infos['title']) + '.html'
    filename = '%s%s' % (folder_path, detail_name)
    with open(filename, 'wb') as f:
        f.write(content_detail)
    infos['html'] = detail_name
    #保存图片
    img_url=i.find_element_by_xpath('./div/div[2]/a/img').get_attribute("src")
    resp_img = requests.get(url=img_url)
    content_img = resp_img.content
    folder_path = "./" + "image" + "/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    img_name = str(infos['title']) + '.jpg'
    filename = '%s%s' % (folder_path, img_name)
    with open(filename, 'wb') as f:
        f.write(content_img)
    infos['img'] = img_name

    print('----',infos)
    return infos


def printInfo(infos, inf):
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='root', db='jh_project01', charset='utf8')

    cur = conn.cursor()
    sqlc = '''
                    create table jrtt(
                    id int primary key auto_increment,
                    title varchar(60),
                    img varchar(60),
                    url varchar(100),
                    html varchar(60))DEFAULT CHARSET=utf8;
                    '''
    try:
        cur.execute(sqlc)
        conn.commit()
        print("成功")
    except:
        print("错误")

    for item, i in enumerate(inf):
        # print(item,i.text)
        if item == 6:
            break
        infos=fillList(infos, i)
        sqla = '''
                insert into jrtt(title,img,url,html)
                values(%s,%s,%s,%s);
               '''
        try:
            cur.execute(sqla, (infos['title'], infos['img'], infos['url'], infos['html']))
            conn.commit()
            print("成功")
        except:
            print("失败")

    conn.commit()
    cur.close()
    conn.close()

def main():
    infos = {}
    driver = webdriver.Chrome()
    driver.get('https://www.toutiao.com/ch/news_tech/')
    js = "var q=document.documentElement.scrollTop=500"
    driver.execute_script(js)
    inf = driver.find_elements_by_xpath('//div[@class="wcommonFeed"]/ul/li[@class="item    "]')
    # print(inf)
    # print(len(inf))
    printInfo(infos,inf)

    driver.close()

main()