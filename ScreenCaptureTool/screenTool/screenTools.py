# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 12:39
# @Author : Matrix
# @File : screenTools.py
# @Software: PyCharm
# ---************************************************---
import pygetwindow as gw
import pyautogui


def get_screen():
    # window = gw.getWindowsWithTitle(f"PID {pid}")
    # window=gw.getWindowsWithTitle('云·原神')
    windows=gw.getAllWindows()
    for window in windows:
        # print(window.title)
        if window.title=='云·原神':
            window.activate()
            window_rect = window.left, window.top, window.width, window.height
            screenshot = pyautogui.screenshot(region=window_rect)# 截取窗口的屏幕内容
            screenshot.save("./data/screenshot.png")# 保存截图为图像文件
            print("屏幕截图已保存为screenshot.png")
            pass
        pass
    # print(windows)
    # if window:
    #     window[0].activate()  # 激活窗口
    #     window_rect = window[0].left, window[0].top, window[0].width, window[0].height  # 获取窗口位置和大小
    #     # screenshot = pyautogui.screenshot(region=window_rect)# 截取窗口的屏幕内容
    #     # screenshot.save("./data/screenshot.png")# 保存截图为图像文件
    #     # print("屏幕截图已保存为screenshot.png")
    # else:
    #     print(f"找不到PID为{pid}的窗口")
    pass
