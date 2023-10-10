# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 10:49
# @Author : Matrix
# @File : get_Pid.py
# @Software: PyCharm
# ---************************************************---
import argparse
import psutil

from ScreenCaptureTool.memeryTool.memeryTools import GameProcess
from ScreenCaptureTool.mouseTool.mouseTools import *


# 获取所有pid
from ScreenCaptureTool.screenTool.screenTools import get_screen


def list_processes():
    for process in psutil.process_iter(['pid', 'name', 'status']):
        try:
            process_info = process.info
            print(f"PID: {process_info['pid']}, Name: {process_info['name']}, Status: {process_info['status']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    pass


# 查询进程名
def get_process(process_name,return_value):
    #
    # """通过进程名获取pid并返回"""
    # process_name 进程名
    # return_value 返回值类别:pid,name,status
    #
    for process in psutil.process_iter(['pid', 'name', 'status']):
        try:
            process_info = process.info
            if process_info['name']==process_name:
                # print(f"PID: {process_info['pid']}, Name: {process_info['name']}, Status: {process_info['status']}")
                match(return_value):
                    case 'pid':
                        return process_info['pid']
                        break
                    case 'name':
                        return process_info['name']
                        break
                    case 'status':
                        return process_info['status']
                        break
                    case _:
                        return process_info['pid']
                        break
                pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    pass
    pass


def main(args):
    # list_processes()

    temp=get_process('Genshin Impact Cloud Game.exe','pid')
    print(temp)
    get_screen()

    # game_process=GameProcess('AppMarket.exe')
    # move_mouse(900, 500)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
