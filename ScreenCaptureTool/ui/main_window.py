# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/12 0012 12:57
# @Author : Matrix
# @File : main_window.py
# @Software: PyCharm
# ---************************************************---
import os
import sys
from functools import partial

import mss
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ScreenCaptureTool.screenTool.screenTools import *


class ScreenRecorderMainUi(QMainWindow):
    def __init__(self, width, height):
        super().__init__()  # 使用super()调用父类构造函数
        self.window_width = width
        self.window_height = height
        self.initUI()
        self.recording = False
        self.screen = QApplication.primaryScreen()
        self.out = None

    def initUI(self):
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setWindowTitle('MatrixCapture')
        # 获取屏幕的大小
        screen = QApplication.desktop().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        # 计算窗口的位置，使其位于屏幕中心
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.setGeometry(x, y, self.window_width, self.window_height)
        # 加载图标文件并设置窗口图标
        icon = QIcon("./resources/head_icon.webp")  # 替换"icon.png"为你的图标文件路径
        self.setWindowIcon(icon)

        self.process_button = QPushButton('获取进程', self)
        self.capture_button = QPushButton('捕获屏幕', self)
        self.stop_button = QPushButton('停止捕获', self)
        self.process_combo_box = QComboBox(self)
        self.process_button.setGeometry(80, 10, 100, 30)
        self.capture_button.setGeometry(190, 10, 100, 30)
        self.stop_button.setGeometry(100, 100, 100, 30)
        self.process_combo_box.setGeometry(80, 50, 240, 30)
        self.process_button.clicked.connect(self.get_process)
        self.capture_button.clicked.connect(self.button_clicked)
        self.stop_button.clicked.connect(self.stop_recording)

        pass

    def get_process(self):
        self.process_combo_box.clear()
        process = get_all_process()
        for temp_list in process:
            self.process_combo_box.addItem(temp_list)
            pass
        pass

    def button_clicked(self):
        if self.process_combo_box.currentText() == '':
            print("进程为空")
            pass
        else:
            print(self.process_combo_box.currentText())
            # get_screen_video(self.process_combo_box.currentText())

            window_title = self.process_combo_box.currentText()
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                # 获取窗口的进程ID（PID）
                pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                print(f"窗口标题为'{window_title}'的窗口句柄为: {hwnd}")
                print(f"对应的进程ID (PID) 为: {pid}")
                # 激活窗口
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                # 延迟1s录制
                time.sleep(1)
                # 获取窗口的尺寸(相对于窗口)
                # client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(hwnd)
                w_left, w_top, w_right, w_bottom = win32gui.GetWindowRect(hwnd)  # 这些值包含了整个窗口的位置信息
                # 视频帧数
                frame_rate = 30.0
                width = w_right - w_left
                height = w_bottom - w_top
                current_time = datetime.datetime.now().timestamp()
                file_name = datetime.datetime.fromtimestamp(current_time).strftime('%Y%m%d-%H-%M-%S')
                print(file_name)
                save_name = './data/' + file_name + '-Capture.mp4'
                print(save_name)

                fourcc = cv2.VideoWriter_fourcc(*'h264')
                self.filename = 'recording_' + datetime.datetime.fromtimestamp(
                    datetime.datetime.now().timestamp()).strftime('%Y%m%d-%H-%M-%S') + '.mp4'
                save_name = './data/' + self.filename
                self.out = cv2.VideoWriter(save_name, fourcc, frame_rate, (width, height))

                # Start recording
                print("录制中...")
                self.recording = True
                while self.recording:
                    try:
                        # frame = numpy.array(sct.grab(self.monitor))
                        screenshot = pyautogui.screenshot(region=(w_left, w_top, width, height))
                        # 将截图转换为OpenCV格式
                        frame = numpy.array(screenshot)
                        # 写入视频
                        self.out.write(frame)
                    except OSError as e:
                        print(f'Error recording video or audio: {e}')
                        self.recording = False
                    # frame = numpy.array(sct.grab(self.monitor))


                # qapp = QApplication.instance()
                # qapp.processEvents()
                # Release video writer
                self.out.release()

            pass

        pass

    def stop_recording(self):
        # Release video writer
        if self.out is not None:
            self.out.release()

        # Stop recording
        self.recording = False
        print("录制结束!")

    pass
