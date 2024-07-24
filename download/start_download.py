# ---************************************************---
# @coding: utf-8
# @Time : 2024/5/29 0029 16:41
# @Author : Matrix
# @File : start_download.py
# @Software: PyCharm
# ---************************************************---
import argparse
import os
import requests


def download():
    # 下载头链接
    base_url = 'https://hw-dts.videocc.net/e03bb44c23/0/1709277515276/f/72/aa/4f_1/e03bb44c231bee12fb6a1581f672aa4f_1_'
    # 起始和结束的数字
    start_number = 0
    end_number = 178
    # 目标文件夹（可选，用于保存下载的文件）
    destination_folder = './download_file'

    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

        # 使用for循环来构建URL并下载文件
    for i in range(start_number, end_number + 1):
        # 格式化文件名（包括末尾的数字）
        filename = f'{i}.ts'
        # 完整的URL
        url = f'{base_url}{i}.ts?pid=1716967640603X1771992&device=desktop'
        # 目标文件路径（包括文件夹和文件名）
        target_path = os.path.join(destination_folder, filename)
        # 发送GET请求获取文件内容
        response = requests.get(url, stream=True)
        # 检查请求是否成功
        if response.status_code == 200:
            # 打开文件以二进制写入模式
            with open(target_path, 'wb') as f:
                # 迭代地写入文件内容
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"文件 {filename} 下载成功！")
        else:
            print(f"请求失败，状态码为：{response.status_code}，URL：{url}")


def main(args):
    download()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filePath', type=str, default='./xxx/xxx', help='文件地址')
    # parser.add_argument('--filePath', type=str, required=True, help='文件地址')
    args = parser.parse_args()
    main(args)
