import requests
import os
import time
import threading
import re
from bs4 import BeautifulSoup

# 替换 大小
pattern = re.compile('\_\d+x\d+\.jpg$')
# 获取 .jpg 前面的id 部分
id_pattern = re.compile('(\d+)\.jpg$')


def download_page(url):
    '''
    用于下载页面
    '''
    r = requests.get(url)
    r.encoding = 'gb2312'
    return r.text


def get_pic_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.select(".container .item .progressive__img")

    for tag in pic_list:
        url = tag.get("src")
        out_src = re.sub(pattern, '.jpg', url)
        img_id = id_pattern.search(out_src).groups()[0]
        get_pic(url, img_id)


def get_pic(link, text):
    '''
    获取当前页面的图片,并保存
    '''
    print(link)
    r = requests.get(link)  # 下载图片，之后保存到文件
    with open('pic/{}.jpg'.format(text), 'wb') as f:
        f.write(r.content)
        time.sleep(1)  # 休息一下，不要给网站太大压力，避免被封


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html)


def main():
    create_dir('pic')  # 创建文件夹
    queue = [i for i in range(1, 5)]  # 构造 url 链接 页码。   # 创建一个以为数组，内容为 1 ~ 4
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and len(queue) > 0:  # 最大线程数设置为 5
            cur_page = queue.pop(0)
            url = 'https://bing.ioliu.cn/?p={}'.format(cur_page)
            # thread = threading.Thread(target=execute, args=(url,), name='第{}线程'.format(cur_page))
            # thread.setDaemon(True)
            # thread.start()
            # print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            # threads.append(thread)

            print('{}正在下载{}页'.format('主线程', cur_page))
            execute(url)


if __name__ == '__main__':
    main()
