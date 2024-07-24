# ---************************************************---
# @coding: utf-8
# @Time : 2024/5/29 0029 17:00
# @Author : Matrix
# @File : build_file_name.py
# @Software: PyCharm
# ---************************************************---
import argparse
import os
import re


def loadFile():
    # 指定要遍历的文件夹路径
    folder_path = 'E:\\Ffmpeg\\bin\\video'  # 替换为你实际的文件夹路径
    file_names = []
    # 遍历文件夹并获取所有文件名
    for filename in os.listdir(folder_path):
        # os.path.isfile() 用于检查是否为文件（排除文件夹）
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_names.append(filename)
            # print(filename)
    print(file_names)
    return file_names

    # 如果你想要包含子文件夹中的文件，可以使用 os.walk()
    # for root, dirs, files in os.walk(folder_path):
    #     for file in files:
    #         print(os.path.join(root, file))


# 使用正则表达式提取文件名中的数字部分，并将其转换为整数以便排序
def extract_number(filename):
    match = re.search(r'(\d+)\.ts', filename)
    if match:
        return int(match.group(1))
    else:
        # 如果没有匹配到数字，可以返回一个很大的数或抛出一个异常，取决于你的需求
        return float('inf')
    # 对文件名列表进行排序，使用自定义的排序键（即提取的数字）


def main(args):
    sorted_filenames = sorted(loadFile(), key=extract_number)
    # 打印排序后的文件名
    # for filename in sorted_filenames:
    #     print(filename)
    # pass
    # 覆盖
    with open(args.file_path,"w+",encoding="utf-8") as filecount:
        for filename in sorted_filenames:
            filecount.write("\n" + "file 'E:\\Ffmpeg\\bin\\video\\"+filename+"'")
            pass
        pass
    filecount.close()
    print('文件写入完成!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default="E:\\Ffmpeg\\bin\\video.txt", help='文件地址')
    # parser.add_argument('--filePath', type=str, required=True, help='文件地址')
    args = parser.parse_args()
    main(args)
