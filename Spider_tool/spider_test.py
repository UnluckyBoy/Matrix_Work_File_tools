# ---************************************************---
# @coding: utf-8
# @Time : 2023/5/11 0011 11:31
# @Author : Matrix
# @File : spider_test.py
# @Software: PyCharm
# ---************************************************---
import argparse
import requests
from bs4 import BeautifulSoup

def get_data():

    url='https://www.jaxhjzx.com/xcplay/58121-3-40.html'
    # url = 'https://mooc1.chaoxing.com/mooc2/work/view?courseId=207331970&classId=75435216&cpi=206522217&workId=27381183&answerId=51772214&enc=dcb3c89b7e0210d9a8b8126f1186f2dc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    pass

def main(args):
    get_data()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
