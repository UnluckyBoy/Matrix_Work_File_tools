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
    url = 'http://quote.eastmoney.com/stocklist.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'

    soup = BeautifulSoup(response.text, 'html.parser')
    stock_list = soup.find('div', {'id': 'quotesearch'}).find_all('a')

    for stock in stock_list:
        code = stock['href'].split('/')[-1].split('.')[0]
        name = stock.text
        print(code, name)
    pass

def main(args):
    get_data()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
