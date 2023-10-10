# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 12:39
# @Author : Matrix
# @File : screenTools.py
# @Software: PyCharm
# ---************************************************---
import pygetwindow as gw
import pyautogui
import win32gui
import win32con
import ctypes
import time
import cv2
import numpy as np
import win32process
import win32ui
import psutil
import time
import pywinauto
import ctypes
from PIL import ImageGrab


def get_screen():
    windows = gw.getAllWindows()
    for window in windows:
        # print(window.title)
        if window.title == '云·原神':
            window.activate()
            time.sleep(1)
            window_rect = window.left, window.top, window.width, window.height
            screenshot = pyautogui.screenshot(region=window_rect)  # 截取窗口的屏幕内容
            screenshot.save("./data/screenshot.png")  # 保存截图为图像文件
            print("屏幕截图已保存为screenshot.png")
            pass
        pass
    pass


def get_screen_2():
    windows = gw.getAllWindows()
    for window in windows:
        if window.title == '云·原神':
            window_handle = window._hWnd
            # 激活窗口
            win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(window_handle)
            time.sleep(1)
            # 获取窗口位置和大小
            window_rect = win32gui.GetWindowRect(window_handle)
            left, top, right, bottom = window_rect
            # 截图窗口的内容
            screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
            # 保存截图为图像文件
            screenshot.save("./data/window_screenshot.png")
            print("窗口截图已保存为window_screenshot.png")
            pass
        pass
    pass


def get_screen_video():
    # 替换为您要获取的窗口的标题
    window_title = '云·原神'
    # 查找窗口句柄
    window_handle = win32gui.FindWindow(None, window_title)
    if window_handle:
        # 获取窗口的进程ID（PID）
        pid = win32process.GetWindowThreadProcessId(window_handle)[1]
        print(f"窗口标题为'{window_title}'的窗口句柄为: {window_handle}")
        print(f"对应的进程ID (PID) 为: {pid}")
    else:
        print(f"找不到标题为'{window_title}'的窗口")
    pass

    # 激活窗口
    win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(window_handle)
    time.sleep(1)

    width, height = psutil.win32gui.GetWindowRect(window_handle)[2:4]
    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img.save('./data/screenshot.png')


    # windows = gw.getAllWindows()
    # for window in windows:
    #     hwnd = win32gui.FindWindow(None, window.title)
    #     if hwnd:
    #         # 获取窗口的进程ID（PID）
    #         pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    #         print(f"窗口标题为'{window.title}'的窗口句柄为: {hwnd}")
    #         print(f"对应的进程ID (PID) 为: {pid}")
    #     else:
    #         print(f"找不到标题为'{window.title}'的窗口")
    #     pass
    pass
