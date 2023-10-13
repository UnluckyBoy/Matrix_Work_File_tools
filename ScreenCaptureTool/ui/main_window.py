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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyaudio
from ScreenCaptureTool.screenTool.screenTools import *
import cv2
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from moviepy.editor import VideoFileClip, AudioFileClip


class ScreenRecorderAudio:
    def __init__(self):
        self.filename = 'recording_' + datetime.datetime.fromtimestamp(
            datetime.datetime.now().timestamp()).strftime('%Y%m%d-%H-%M-%S') + '.wav'
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

        audio_save_name = './data/' + self.filename

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
            file_name = datetime.datetime.fromtimestamp(current_time).strftime('%Y%m%d-%H-%M-%S')
            print(file_name)
            save_name = './data/' + file_name + '-Capture.mp4'
            print(save_name)

            sct = mss.mss()
            fourcc = cv2.VideoWriter_fourcc(*'h264')
            self.filename = 'recording_' + datetime.datetime.fromtimestamp(
                datetime.datetime.now().timestamp()).strftime('%Y%m%d-%H-%M-%S') + '.mp4'
            save_name = './data/' + self.filename
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

        video_file = self.filename
        audio_file = self.audio_recorder.filename
        video_path = None
        audio_path = None
        for file in os.listdir('./data/'):
            if file.endswith(".mp4") and file == video_file:
                video_path = file
            elif file.endswith(".wav") and file == audio_file:
                audio_path = file
        if video_path is None or audio_path is None:
            QMessageBox.warning(self, "Error", "音频或者视频文件不存在!")
            return
        video = VideoFileClip(video_path).set_fps(self.frame_rate).resize(self.duration)
        audio = AudioFileClip(audio_path)
        print('视频时长:', video.duration)
        print('音频时长:', audio.duration)
        final_video = video.set_audio(audio)

        video1 = cv2.VideoCapture(self.filename)
        old_fps = video1.get(CAP_PROP_FPS)
        Count = video1.get(CAP_PROP_FRAME_COUNT)
        size = (int(video1.get(CAP_PROP_FRAME_WIDTH)), int(video1.get(CAP_PROP_FRAME_HEIGHT)))
        print('视频帧率=%.1f' % old_fps)
        print('视频的帧数=%.1f' % Count)
        print('视频的分辨率', size)
        print('视频时间=%.3f秒' % (int(Count) / old_fps))
        print('视频的录制时间=%.3f秒' % (audio.duration))
        new_fps = old_fps * (int(Count) / old_fps) / (audio.duration)
        print('推荐帧率=%.2f' % (new_fps))
        final_video.write_videofile("./data/final_video.mp4", fps=new_fps, codec='libx264', audio_codec='aac')

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
