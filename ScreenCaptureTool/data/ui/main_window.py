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

import mss
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyaudio
from ScreenCaptureTool.data.screenTool.screenTools import *
import cv2
import moviepy.editor as mp


# 得到当前执行文件同级目录的其他文件绝对路径
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('')
    return os.path.join(base_path, relative_path)


class ScreenRecorderAudio:
    def __init__(self):
        self.audio_file_name = 'recording_' + datetime.datetime.fromtimestamp(
            datetime.datetime.now().timestamp()).strftime('%Y%m%d-%H%M%S') + '.wav'
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

        audio_save_name = './data/' + self.audio_file_name

        with wave.open(audio_save_name, 'wb') as waveFile:
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.frames))

        print(f'音频录制 {len(self.frames)} 帧')

    def record(self):
        try:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            # print(f'Recorded {len(data)} bytes')
        except OSError as e:
            print(f'音频录制异常: {e}')
            self.flush()


class ScreenRecorderMainUi(QMainWindow):
    def __init__(self, width, height):
        super().__init__()  # 使用super()调用父类构造函数
        self.window_width = width
        self.window_height = height
        self.screen = QApplication.primaryScreen()
        # 视频帧数
        self.frame_rate = 30
        self.initUI()
        self.out = None
        # 创建音频对象
        self.audio_recorder = ScreenRecorderAudio()
        self.icon_quit()

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
        # 显示默认时长
        self.resolution_text_label = QLabel("默认时长(分):", self)
        self.resolution_text_label.setGeometry(80, 90, 200, 30)
        self.resolution_text_edit = QLineEdit(self)
        self.resolution_text_edit.setPlaceholderText('5')
        self.resolution_text_edit.setGeometry(200, 90, 60, 30)

        self.process_button = QPushButton('获取进程', self)
        self.capture_button = QPushButton('捕获屏幕', self)
        self.stop_button = QPushButton('停止捕获', self)

        self.process_combo_box = QComboBox(self)
        self.process_button.setGeometry(80, 10, 100, 30)
        self.capture_button.setGeometry(190, 10, 100, 30)
        self.stop_button.setGeometry(300, 10, 100, 30)
        self.process_combo_box.setGeometry(80, 50, 320, 30)
        self.capture_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.process_button.clicked.connect(self.get_process)
        self.capture_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

    def get_process(self):
        self.process_combo_box.clear()
        process = get_all_process()
        for temp_list in process:
            self.process_combo_box.addItem(temp_list)
        self.capture_button.setEnabled(True)

    def start_recording(self):
        self.stop_button.setEnabled(True)
        self.capture_button.setEnabled(False)

        self.recording_text_label.setText("录制中...")
        self.recording_timer.start(300)  # 每0.3秒闪一次
        self.audio_recorder.start()
        if self.resolution_text_edit.text() == '':
            self.duration = 300
        else:
            self.duration = int(self.resolution_text_edit.text()) * 60
        start_time = time.time()
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
            width = w_right - w_left
            height = w_bottom - w_top
            current_time = datetime.datetime.now().timestamp()
            file_name = datetime.datetime.fromtimestamp(current_time).strftime('%Y%m%d-%H%M%S')
            print(file_name)
            save_name = './data/' + file_name + '-Capture.mp4'
            print(save_name)

            sct = mss.mss()
            fourcc = cv2.VideoWriter_fourcc(*'h264')
            self.video_file_name = 'recording_' + datetime.datetime.fromtimestamp(
                datetime.datetime.now().timestamp()).strftime('%Y%m%d-%H-%M-%S') + '.mp4'
            save_name = './data/' + self.video_file_name
            self.out = cv2.VideoWriter(save_name, fourcc, self.frame_rate, (width, height))
            target_screen = {"top": w_top, "left": w_left, "width": width, "height": height}
            # 开始录制
            self.recording = True
            while self.recording:
                try:
                    # screenshot = pyautogui.screenshot(region=(w_left, w_top, width, height))
                    # # 将截图转换为OpenCV格式
                    # frame = numpy.array(screenshot)
                    # 使用mss录制
                    frame = numpy.array(sct.grab(target_screen))
                    if frame.size == 0:
                        continue
                    # print("Before conversion:", frame.shape)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    # 写入视频
                    self.out.write(frame)
                    self.audio_recorder.record()
                    if time.time() - start_time >= self.duration:
                        self.recording = False
                        self.audio_recorder.stop()
                        self.recording_text_label.setText("录制结束")
                        self.recording_timer.stop()
                        self.recording_piont_label.hide()
                        break
                except OSError as e:
                    print(f'录制异常: {e}')
                    self.recording = False
                    self.audio_recorder.flush()
                app = QApplication.instance()  # 设置在while循环中窗口可控
                app.processEvents()
            # 释放video writer
            self.out.release()
            sct.close()

    def stop_recording(self):
        # 释放 video writer
        if self.out is not None:
            self.out.release()

        # Stop recording
        self.recording = False
        self.recording_text_label.setText("录制结束")
        self.recording_timer.stop()
        self.recording_piont_label.hide()
        self.audio_recorder.stop()
        self.capture_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        output_video_file = './data/' + self.video_file_name
        output_audio_file = './data/' + self.audio_recorder.audio_file_name
        video_clip = mp.VideoFileClip(output_video_file)
        audio_clip = mp.AudioFileClip(output_audio_file)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile('./data/' + self.video_file_name[:-4].replace('recording', 'capture') + '.mp4',
                                   codec='libx264', audio_codec='aac')

        # # 清理临时文件
        os.remove(output_video_file)
        os.remove(output_audio_file)

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

    def icon_quit(self):
        # 托盘
        mini_icon = QtWidgets.QSystemTrayIcon(self)
        mini_icon.setIcon(QtGui.QIcon(get_resource_path(os.path.join("resources", "head_icon.png"))))
        mini_icon.setToolTip("MatrixCapture")
        # 为托盘增加一个菜单选项
        tpMenu = QtWidgets.QMenu(self)
        # 为菜单指定一个选项
        quit_menu_Auth = QtWidgets.QAction('作者', self, triggered=self.open_auth)
        tpMenu.addAction(quit_menu_Auth)
        quit_menu = QtWidgets.QAction('退出', self, triggered=self.quit)
        tpMenu.addAction(quit_menu)

        mini_icon.setContextMenu(tpMenu)
        mini_icon.show()

    def open_auth(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/UnluckyBoy/Matrix_Work_File_tools'))

    def quit(self):
        self.close()
        sys.exit()
