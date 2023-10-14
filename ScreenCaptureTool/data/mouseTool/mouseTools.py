# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 11:10
# @Author : Matrix
# @File : mouseTools.py
# @Software: PyCharm
# ---************************************************---
import win32api
import win32con
import win32gui


# 模拟鼠标移动到指定位置
def move_mouse(x, y):
    win32api.SetCursorPos((x, y))


# 模拟鼠标左键点击
def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


# 模拟鼠标右键点击
def right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


# 模拟鼠标滚轮滚动
def scroll_wheel(delta):
    # 使用win32gui获取当前窗口句柄，如果不需要，可以省略这一步
    hwnd = win32gui.GetForegroundWindow()
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta, hwnd)
