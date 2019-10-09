# coding:utf-8


import requests
from bs4 import BeautifulSoup

# 获取 必应上的 html 数据
r = requests.get(url='https://bing.ioliu.cn/').text
# 对获取到的文本进行解析
soup = BeautifulSoup(r,'lxml')
# 从解析文件中通过select选择器定位指定的元素，返回一个列表
img_tags = soup.select(".container .item .progressive__img")

# 对返回的列表进行遍历
for n in img_tags:
    print(n.get("src"))


print "123"
