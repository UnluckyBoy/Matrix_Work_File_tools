# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/12 0012 12:57
# @Author : Matrix
# @File : main_window.py
# @Software: PyCharm
# ---************************************************---
import os
import sys
import wave
from functools import partial

import mss
from PIL import ImageGrab
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyaudio
from ScreenCaptureTool.screenTool.screenTools import *


class ScreenRecorderAudio:
    def __init__(self, filename):
        self.filename = f'recording_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.wav'
        self.chunk = 2048
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.input_device_index = self.audio.get_default_input_device_info()['index']
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True, input_device_index=self.input_device_index,
                                      frames_per_buffer=self.chunk)

    def start(self):
        self.frames = []
        self.stream.start_stream()
        self.frames.append(self.stream.read(self.chunk))

    def flush(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.frames = []

    def stop(self):
        if self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()

        audio_save_name = './dada/' + self.filename

        with wave.open(audio_save_name, 'wb') as waveFile:
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.frames))

        print(f'Recorded {len(self.frames)} frames')

    def record(self):
        try:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            # print(f'Recorded {len(data)} bytes')
        except OSError as e:
            print(f'Error recording audio: {e}')
            self.flush()


class ScreenRecorderMainUi(QMainWindow):
    def __init__(self, width, height):
        super().__init__()  # 使用super()调用父类构造函数
        self.window_width = width
        self.window_height = height
        self.screen = QApplication.primaryScreen()
        # self.initUI()

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

        # 录制显示
        self.recording_text_label = QLabel("未录制", self)
        self.recording_text_label.setGeometry(80, 130, 200, 30)
        # 录制闪烁点
        self.recording_piont_label = QLabel(self)
        self.recording_piont_label.setGeometry(180, 135, 20, 20)
        self.recording_piont_label.setStyleSheet("background-color: red; border-radius: 10px;")
        self.recording_piont_label.hide()
        # 创建录制闪烁定时器
        self.recording_timer = QTimer(self)
        self.recording_timer.timeout.connect(self.toggle_recording_point)

        self.process_button = QPushButton('获取进程', self)
        self.capture_button = QPushButton('捕获屏幕', self)
        self.stop_button = QPushButton('停止捕获', self)
        self.process_combo_box = QComboBox(self)
        self.process_button.setGeometry(80, 10, 100, 30)
        self.capture_button.setGeometry(190, 10, 100, 30)
        self.stop_button.setGeometry(100, 90, 100, 30)
        self.process_combo_box.setGeometry(80, 50, 240, 30)
        self.process_button.clicked.connect(self.get_process)
        self.capture_button.clicked.connect(self.start_recording)
        # self.recording_timer.start(300)
        self.stop_button.clicked.connect(self.stop_recording)

        self.out = None

    def get_process(self):
        self.process_combo_box.clear()
        process = get_all_process()
        for temp_list in process:
            self.process_combo_box.addItem(temp_list)

    def start_recording(self):
        if self.process_combo_box.currentText() == '':
            print("进程为空")
        else:
            print("录制中...")
            print(self.process_combo_box.currentText())
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
                # time.sleep(1)
                # 获取窗口的尺寸(相对于窗口)
                # client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(hwnd)
                w_left, w_top, w_right, w_bottom = win32gui.GetWindowRect(hwnd)  # 这些值包含了整个窗口的位置信息
                # 视频帧数
                frame_rate = 30
                width = w_right - w_left
                height = w_bottom - w_top
                current_time = datetime.datetime.now().timestamp()
                file_name = datetime.datetime.fromtimestamp(current_time).strftime('%Y%m%d-%H-%M-%S')
                print(file_name)
                save_name = './data/' + file_name + '-Capture.mp4'
                print(save_name)

                start_time = time.time()
                fourcc = cv2.VideoWriter_fourcc(*'h264')
                self.filename = 'recording_' + datetime.datetime.fromtimestamp(
                    datetime.datetime.now().timestamp()).strftime('%Y%m%d-%H-%M-%S') + '.mp4'
                save_name = './data/' + self.filename
                self.out = cv2.VideoWriter(save_name, fourcc, frame_rate, (width, height))

                # 开始录制
                self.recording = True
                while self.recording:
                    screenshot = pyautogui.screenshot(region=(w_left, w_top, width, height))
                    # 将截图转换为OpenCV格式
                    frame = numpy.array(screenshot)
                    # 写入视频
                    self.out.write(frame)
                    if time.time() - start_time >= 10:
                        self.recording = False
                        self.recording_text_label.setText("录制结束")
                        break
                    app = QApplication.instance()  # 设置在while循环中窗口可控
                    app.processEvents()

                # 释放video writer
                self.out.release()

    def stop_recording(self):
        # Release video writer
        if self.out is not None:
            self.out.release()

        # Stop recording
        self.recording = False
        self.recording_text_label.setText("录制结束")
        self.recording_timer.stop()
        self.recording_piont_label.hide()

    def toggle_recording_point(self):
        # 切换记录闪烁点可见性
        if self.recording_piont_label.isVisible():
            self.recording_piont_label.hide()
        else:
            self.recording_piont_label.show()

    def paintEvent(self, event):
        # 绘制录制闪烁灯
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.recording_piont_label.isVisible():
            painter.setBrush(QColor(255, 0, 0))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(180, 135, 20, 20)
