# ---************************************************---
# @coding: utf-8
# @Time : 2023/3/28 0028 12:35
# @Author : Matrix
# @File : do_start.py
# @Software: PyCharm
# 批量命名文件
# ---************************************************---
import argparse
import os

import pandas as pd


def LoadFile(filepath):
    with open(filepath,"a+",encoding="utf-8") as filecount:
        for i in range(157):
            filecount.write("\n" + "file 'E:\\Ffmpeg\\bin\\video\\"+str(i)+".ts'")
            pass
        # print(test)
        pass
    filecount.close()
    pass


def main(args):
    LoadFile(args.file_path)
    # LoadFile()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default="E:\\Ffmpeg\\bin\\video.txt", help='文件地址')
    args = parser.parse_args()
    main(args)
