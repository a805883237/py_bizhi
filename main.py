# coding:utf-8

#CREATE TABLE data(img_key VARCHAR(), src VARCHAR() , source_url VARCHAR())

import requests
from bs4 import BeautifulSoup
import re
import pymysql

# 数据库处理
# 创建游标
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='*******',db='bing_bizhi',charset='utf8')
# 创建游标
cursor = conn.cursor()

print "数据库连接已创建"

# 获取 必应上的 html 数据
r = requests.get(url='https://bing.ioliu.cn/').text
# 对获取到的文本进行解析
soup = BeautifulSoup(r,'lxml')
# 从解析文件中通过select选择器定位指定的元素，返回一个列表
img_tags = soup.select(".container .item .progressive__img")


# 替换 大小
pattern = re.compile(ur'\_\d+x\d+\.jpg$')
# 获取 .jpg 前面的id 部分
id_pattern = re.compile(ur'(\d+)\.jpg$')


# 对返回的列表进行遍历
for n in img_tags:
    url = n.get("src")
    out_src = re.sub(pattern,'.jpg',url)
    #print(out_src)
    img_id = id_pattern.search(out_src).groups()[0]
    print(img_id)
    #print(url)
    # 存入数据库
    cursor.execute("INSERT INTO data(img_key,src,source_url)VALUES('{0}','{1}','{2}');".format(img_id,out_src,url))
    conn.commit()


print "数据库连接已关闭"
cursor.close()
conn.close()
