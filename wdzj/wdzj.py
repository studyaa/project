import time
import csv
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup


def wdzj_spider(uname,pwd):
    #隐藏界面
    display = Display(visible=0, size=(800, 600))
    display.start()

    driver=webdriver.Chrome()
    driver.get('https://shuju.wdzj.com/problem-1.html')

    driver.find_element_by_xpath('//div[@id="tableTmpl"]/a').click()

    driver.find_element_by_xpath('//input[@id="logusername"]').send_keys(str(uname))
    driver.find_element_by_xpath('//input[@id="logpassword"]').send_keys(str(pwd))
    driver.find_element_by_xpath('//input[@id="autcheck"]').click()
    driver.find_element_by_xpath('//a[@class="login-button logReg_btn1"]').click()
    time.sleep(3)

    content=driver.page_source
    bs=BeautifulSoup(content,'lxml')
    pt_list=bs.select('tr[class],tr[class=cl]')
    info_list=[]
    for pt in pt_list:
        info = {}
        info['序号'] = pt.find_all('td')[0].text.strip()
        info['平台'] = pt.find_all('td')[1].text.strip()
        info['问题时间'] = pt.find_all('td')[2].text.strip()
        info['上线时间'] = pt.find_all('td')[3].text.strip()
        info['注册资本(万元)'] = pt.find_all('td')[4].text.strip()
        info['地区'] = pt.find_all('td')[5].text.strip()
        info['事件类型'] = pt.find_all('td')[6].text.strip()
        info_list.append(info)

        keys = info_list[0].keys()
        values = [i.values() for i in info_list]
        writer = csv.writer(open('./wdzj.csv', 'w', encoding='utf-8'))
        writer.writerow(keys)
        writer.writerows(values)

    # input('回车继续')
    driver.close()
if __name__ == '__main__':
    uname=input('请输入用户名')
    pwd=input('请输入密码')

    wdzj_spider(uname,pwd)