# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/11 0011 14:27
# @Author : Matrix
# @File : main_ui.py
# @Software: PyCharm
# ---************************************************---
import argparse
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from ScreenCaptureTool.screenTool.screenTools import *


class CaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MatrixCapture")
        self.init_main_layout()
        pass

    def init_main_layout(self):
        # 创建主布局为水平布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)  # 主布局间距
        # 创建垂直布局
        process_list_layout = QVBoxLayout()
        other_layout = QVBoxLayout()

        main_layout.addLayout(process_list_layout)
        main_layout.addLayout(other_layout)

        # # 创建下拉菜单
        label = QLabel("测试")
        process_combo_box = QComboBox()
        # 向下拉菜单中添加选项
        # combo_box.addItem("选项1")
        # combo_box.addItem("选项2")
        # combo_box.addItem("选项3")
        # # 创建按钮
        process_button = QPushButton("获取进程")
        button = QPushButton("测试")

        process_combo_box.setMinimumWidth(450)
        process_button.setMaximumWidth(100)  # 设置按钮的最大宽度为 100 像素
        # 设置下拉菜单的对齐方式
        process_combo_box.setAlignment(Qt.AlignHCenter)  # 水平居中对齐
        process_combo_box.setAlignment(Qt.AlignTop)  # 顶部对齐
        # 设置按钮的对齐方式
        process_button.setAlignment(Qt.AlignHCenter)  # 水平居中对齐
        process_button.setAlignment(Qt.AlignBottom)  # 底部对齐

        # 定义按钮的点击事件,并向下拉菜单中添加选项
        def on_button_click():
            process_combo_box.clear()
            process = get_process()
            for temp_list in process:
                process_combo_box.addItem(temp_list)
                pass

        # 将按钮的点击事件与处理函数关联
        process_button.clicked.connect(on_button_click)

        # 添加控件进布局
        process_list_layout.addWidget(process_combo_box)
        process_list_layout.addWidget(process_button)
        other_layout.addWidget(label)
        other_layout.addWidget(button)

        # 将布局设置为窗口的主要布局
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        pass

    pass
