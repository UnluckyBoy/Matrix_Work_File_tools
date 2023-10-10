# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 10:49
# @Author : Matrix
# @File : get_Pid.py
# @Software: PyCharm
# ---************************************************---
import argparse
import psutil
from ScreenCaptureTool.mouseTool.mouseTools import *


def list_processes():
    for process in psutil.process_iter(['pid', 'name', 'status']):
        try:
            process_info = process.info
            print(f"PID: {process_info['pid']}, Name: {process_info['name']}, Status: {process_info['status']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    pass


def main(args):
    # list_processes()
    move_mouse(900, 500)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
