# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 12:39
# @Author : Matrix
# @File : screenTools.py
# @Software: PyCharm
# ---************************************************---
import pygetwindow as gw
import pyautogui


def get_screen(pid):
    window = gw.getWindowsWithTitle(f"PID: {pid}")
    if window:
        # 激活窗口
        window[0].activate()
        # 获取窗口位置和大小
        window_rect = window[0].left, window[0].top, window[0].width, window[0].height
        # 截取窗口的屏幕内容
        screenshot = pyautogui.screenshot(region=window_rect)
        # 保存截图为图像文件
        screenshot.save("./data/screenshot.png")
        print("屏幕截图已保存为screenshot.png")
    else:
        print(f"找不到PID为{pid}的窗口")
    pass
