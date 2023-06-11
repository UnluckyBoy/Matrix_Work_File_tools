# ---************************************************---
# @coding: utf-8
# @Time : 2023/5/12 0012 13:30
# @Author : Matrix
# @File : apider_music.py
# @Software: PyCharm
# ---************************************************---
import argparse
import requests
from bs4 import BeautifulSoup

def get_music(name):
    music_name=name
    url = "https://www.kugou.com/mixsong/grgj8b3.html?fromsearch={}".format(music_name)
    # music_id=102095
    # url="https://www.51miz.com/so-sound/{}.html".format(music_id)#音效网
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.content
    # print(html)
    # 解析网页内容
    soup = BeautifulSoup(html, "html.parser")
    # data=soup.find(class_="music")
    data=soup.find("audio")
    # print("结果:", soup)
    print("结果:",data)
    pass

def main(args):
    get_music("桃花诺")
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
