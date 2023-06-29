# ---************************************************---
# @coding: utf-8
# @Time : 2023/6/29 0029 14:09
# @Author : Matrix
# @File : start.py
# @Software: PyCharm
# ---************************************************---
import argparse
import urllib.request
import json


def get_head_url(config_path,key):
    result=''
    with open(config_path, 'r') as file:
        json_data = json.load(file)  # 读取JSON文件内容
        # print(json_data[key])
        result=json_data[key]
        pass
    return result
    pass


def get_url(url_path,file_name):
    """#读取所有音频文件地址"""
    path=url_path+file_name+'_url.txt'
    url_result = []
    with open(path, 'r') as file:
        lines = file.readlines()  # 读取文件行
        # print(len(lines))
        for line in lines:
            line = line.strip()  # 去除行尾
            url_result.append(line)
            pass
        pass
    return url_result
    pass


def get_download(head_url, url_list,save_path,file_name):
    """#下载文件"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for index in range(len(url_list)):
        url = head_url+url_list[index]
        # print("文件url", url)
        file_path=save_path+file_name+str(index)+'.mp3'
        print("下载url:", url)
        urllib.request.urlretrieve(url, file_path)
        pass
    # save_path = 'path/to/save/file.txt'  # 要保存的文件路径
    # urllib.request.urlretrieve(url, save_path)
    # print("文件已下载并保存到", save_path)
    pass


def main(args):
    # hutao_head_url = 'https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/4521515/'  # 下载头url
    # sanbing_head_url='https://uploadstatic.mihoyo.com/ys-obc/2022/12/07/16576950/'

    file_name = 'sanbing'  # 文件名***很重要,此对象决定下载的内容、名称等***

    head_url=get_head_url(args.json_path,file_name)
    url_list = get_url(args.url_path,file_name)
    # print(url_list)
    get_download(head_url,url_list,args.download_path,file_name)
    print("！！！文件已下载完成！！！")
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str, default='./data/head_url.json', help='文件地址')
    parser.add_argument('--url_path', type=str, default='./data/', help='文件地址')
    parser.add_argument('--download_path', type=str, default='./data/download/', help='下载地址')
    args = parser.parse_args()
    main(args)
