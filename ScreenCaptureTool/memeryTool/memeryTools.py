# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 11:24
# @Author : Matrix
# @File : memeryTools.py
# @Software: PyCharm
# ---************************************************---
import pymem


class GameProcess:
    def __init__(self, process_name):
        self.process_name = process_name
        pass

    # 打开游戏进程
    def open_game_process(self):
        # self.process_name = "your_game.exe"  # 替换为您的游戏进程名称
        pm = pymem.Pymem(self.process_name)
        pm.open_process()
        # 读取游戏内存中的整数值
        # address = 0x12345678  # 替换为您要读取的内存地址
        # value = pm.read_int(address)
        # print(f"Value at address {hex(address)}: {value}")

    # 关闭进程
    def close_game_process(self):
        pymem.Pymem(self.process_name).close_process()
