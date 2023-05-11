# ---************************************************---
# @coding: utf-8
# @Time : 2023/5/11 0011 10:24
# @Author : Matrix
# @File : spider_weather.py
# @Software: PyCharm
# ---************************************************---
import argparse
import requests
from bs4 import BeautifulSoup
import re

def get_weather_data():

    # 设置要爬取的城市和日期
    city = "榕江"
    date = "20230511"
    id="101260516"
    # 构造URL
    # url = "http://www.weather.com.cn/weather/{}/{}.shtml".format(date, city)
    url = "http://www.weather.com.cn/weather1d/{}.shtml".format(id)
    # 发送请求并获取网页内容
    response = requests.get(url)
    html = response.content
    # print(html)
    # 解析网页内容
    soup = BeautifulSoup(html, "html.parser")
    weather = soup.find(class_="wea").text
    temperature = soup.find(class_="tem").text
    wind_name=soup.find(class_="win").find("i")
    wind=soup.find(class_="win").text
    # 打印天气信息
    print("城市：", city)
    print("日期：", date)
    print("天气：", weather)
    print("温度：", temperature.replace("\n",""))
    # print("风向_测试：", wind_name)
    # print("风向_测试：", len(str(wind_name)))
    # print("风向_测试：", str(wind_name)[10])
    print("风向：", str(wind_name)[10]+","+wind.replace("\n",""))
    pass

def main(args):
    get_weather_data()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
