# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 14:25
# @Author : Matrix
# @File : main_start.py
# @Software: PyCharm
# ---************************************************---
import argparse

from ScreenCaptureTool.screenTool.screenTools import get_screen


def main(args):
    get_screen()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
