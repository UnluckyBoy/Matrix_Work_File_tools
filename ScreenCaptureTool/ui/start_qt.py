# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/12 0012 12:28
# @Author : Matrix
# @File : start_qt.py
# @Software: PyCharm
# ---************************************************---
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QSlider
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
import cv2
import mss
import numpy as np
import time
from datetime import datetime
import pyaudio
import wave
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import os
from moviepy.editor import *
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


class AudioRecorder:
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

        with wave.open(self.filename, 'wb') as waveFile:
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


class RecorderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = None  # Add class attribute
        screen_resolution = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        self.now_time = None

        # Create label for recording indicator
        self.recording_label = QLabel(self)
        self.recording_label.setGeometry(180, 10, 20, 20)
        self.recording_label.setStyleSheet("background-color: red; border-radius: 10px;")
        self.recording_label.hide()

        # Create timer for blinking recording indicator
        self.recording_timer = QTimer(self)
        self.recording_timer.timeout.connect(self.toggle_recording_indicator)

        # Create resolution options
        resolution_label = QLabel("Resolution:", self)
        resolution_label.move(20, 20)
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems(["1080p", "2k", "4k"])
        self.resolution_combo.move(100, 20)

        # Create frame rate options
        framerate_label = QLabel("Frame Rate:", self)
        framerate_label.move(20, 60)
        self.framerate_combo = QComboBox(self)
        self.framerate_combo.addItems(["30Hz", "60Hz", "120Hz"])
        self.framerate_combo.move(100, 60)

        # Create start/stop recording buttons
        self.start_button = QPushButton("Start Recording", self)
        self.start_button.move(20, 100)
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.move(150, 100)
        self.stop_button.clicked.connect(
            lambda: self.stop_recording(self.framerate_combo.currentText(), self.resolution_combo.currentText(),
                                        self.filename))

        # Create duration slider
        self.duration_slider = QSlider(Qt.Horizontal, self)
        self.duration_slider.setGeometry(20, 140, 250, 20)
        self.duration_slider.setMinimum(2)
        self.duration_slider.setMaximum(120)
        self.duration_slider.setValue(60)
        self.duration_slider.setTickPosition(QSlider.TicksBelow)
        self.duration_slider.setTickInterval(5)
        self.duration_slider_label = QLabel("Recording Duration: " + str(self.duration_slider.value()) + "min", self)
        self.duration_slider_label.move(20, 180)
        self.duration_slider.valueChanged.connect(self.update_duration_label)

        # Set window properties
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Recorder GUI")
        self.show()
        self.monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}
        self.sct = mss.mss()
        self.out = None

        # Create audio recorder
        self.audio_recorder = AudioRecorder('recording.wav')

    def update_duration_label(self):
        self.duration_slider_label.setText("Recording Duration: " + str(self.duration_slider.value()) + "min")

    def start_recording(self, filename):
        self.filename = filename
        # Display pop-up message
        QMessageBox.information(self, "Recording", "Recording started. Have fun recording!")

        # Start audio recording
        self.audio_recorder.start()

        # Get start time and duration
        start_time = time.time()
        duration = self.duration_slider.value() * 60
        resolution = self.resolution_combo.currentText()
        selected_resolution = self.resolution_combo.currentText()
        framerate = self.framerate_combo.currentText()
        # Start blinking recording indicator
        self.recording_timer.start(300)

        if selected_resolution == "1080p":
            self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        elif selected_resolution == "2k":
            self.monitor = {"top": 0, "left": 0, "width": 2560, "height": 1440}
        elif selected_resolution == "4k":
            self.monitor = {"top": 0, "left": 0, "width": 3840, "height": 2160}

        sct = mss.mss()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        if resolution == "1080p":
            resolution = (1920, 1080)
        elif resolution == "2k":
            resolution = (2560, 1440)
        elif resolution == "4k":
            resolution = (3840, 2160)
        else:
            raise ValueError("Invalid resolution selected")
        self.filename = f'recording_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.mp4'
        self.out = cv2.VideoWriter(self.filename, fourcc, int(framerate[:-2]), resolution)

        # Start recording
        self.recording = True
        while self.recording:
            try:
                frame = np.array(sct.grab(self.monitor))
                if frame.size == 0:
                    continue
                # print("Before conversion:", frame.shape)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                # print("After conversion:", frame.shape)
                self.out.write(frame)
                # print("before Recorded bytes")
                self.audio_recorder.record()
                # Check if recording has been stopped by user or duration has been reached
                if time.time() - start_time >= duration:
                    self.recording = False
                    # Stop audio recording
                    self.audio_recorder.stop()
            except OSError as e:
                print(f'Error recording video or audio: {e}')
                self.recording = False
                self.audio_recorder.flush()

            qapp = QApplication.instance()
            qapp.processEvents()

        # Release video writer
        if self.out is not None:
            self.out.release()

        # Release screen capture
        if self.sct is not None:
            self.sct.close()

    def stop_recording(self, framerate, resolution, filename):
        # Stop blinking recording indicator
        self.recording_timer.stop()
        self.recording_label.hide()
        # Stop audio recording
        self.audio_recorder.stop()
        # Display pop-up message
        QMessageBox.information(self, "Done", "Recording is finished!")
        # Stop recording
        self.recording = False

        # Release video writer
        if self.out is not None:
            self.out.release()

        # Release screen capture
        if self.sct is not None:
            self.sct.close()
        if resolution == "1080p":
            resolution = (1920, 1080)
        elif resolution == "2k":
            resolution = (2560, 1440)
        elif resolution == "4k":
            resolution = (3840, 2160)
        else:
            raise ValueError("Invalid resolution selected")
            # Merge audio and video files
        video_file = self.filename
        audio_file = self.audio_recorder.filename
        video_path = None
        audio_path = None
        for file in os.listdir():
            if file.endswith(".mp4") and file == video_file:
                video_path = file
            elif file.endswith(".wav") and file == audio_file:
                audio_path = file
        if video_path is None or audio_path is None:
            QMessageBox.warning(self, "Error", "Could not find video or audio file!")
            return
        video = VideoFileClip(video_path).set_fps(int(framerate[:-2])).resize(resolution)
        audio = AudioFileClip(audio_path)
        print('Video duration:', video.duration)
        print('Audio duration:', audio.duration)
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
        final_video.write_videofile("final_video.mp4", fps=new_fps, codec='libx264', audio_codec='aac')

    def toggle_recording_indicator(self):
        # Toggle visibility of recording indicator
        if self.recording_label.isVisible():
            self.recording_label.hide()
        else:
            self.recording_label.show()

    def paintEvent(self, event):
        # Draw recording indicator on top of the widget
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.recording_label.isVisible():
            painter.setBrush(QColor(255, 0, 0))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(180, 10, 20, 20)


if __name__ == '__main__':
    app = QApplication([])
    recorder_gui = RecorderGUI()
    app.exec_()
