# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 12:39
# @Author : Matrix
# @File : screenTools.py
# @Software: PyCharm
# ---************************************************---
import pygetwindow as gw
import pyautogui
import cv2
import numpy
import win32con
import win32gui
import win32process
import win32ui
import psutil
import time


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
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        # 获取窗口的进程ID（PID）
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        print(f"窗口标题为'{window_title}'的窗口句柄为: {hwnd}")
        print(f"对应的进程ID (PID) 为: {pid}")

        # 激活窗口
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        # 获取窗口的尺寸
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        frame_rate = 30.0
        width = right - left
        height = bottom - top
        # 创建VideoWriter对象以保存视频
        fourcc = cv2.VideoWriter_fourcc(*'h264')  # avi格式:XVID;mp4格式:mp4v,h264
        out = cv2.VideoWriter('./data/output.mp4', fourcc, frame_rate, (width, height))
        while True:
            # 使用pyautogui截图窗口内容
            screenshot = pyautogui.screenshot(region=(left, top, right, bottom))
            # 将截图转换为OpenCV格式
            frame = numpy.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 写入视频
            out.write(frame)
            cv2.imshow("Window Recording", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        out.release()
        cv2.destroyAllWindows()

    else:
        print(f"找不到标题为'{window_title}'的窗口")
    pass

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
