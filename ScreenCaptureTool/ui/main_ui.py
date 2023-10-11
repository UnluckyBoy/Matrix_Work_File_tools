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
from functools import partial

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

        # 创建小部件用作子布局的背景
        process_layout_widget = QWidget()
        other_layout_widget = QWidget()
        # 创建子布局为垂直布局
        process_list_layout = QVBoxLayout()
        other_layout = QVBoxLayout()

        # 将布局设置为窗口的主要布局
        main_widget = QWidget()
        main_layout.addWidget(process_layout_widget)
        main_layout.addWidget(other_layout_widget)
        main_widget.setLayout(main_layout)
        # 设置布局的背景颜色
        # main_widget.setStyleSheet("background-color: lightblue;")
        self.setCentralWidget(main_widget)
        self.init_process_layout(process_layout_widget, process_list_layout)
        self.init_other_layout(other_layout_widget, other_layout)
        pass

    @staticmethod
    def init_process_layout(process_layout_widget, process_list_layout):
        """
        # 加载进程布局视图
        :param process_layout_widget:进程布局的背景组件
        :param process_list_layout:进程布局
        :return:
        """
        # 将子布局添加到子部件
        process_layout_widget.setLayout(process_list_layout)
        # 设置子布局的背景颜色
        process_layout_widget.setStyleSheet("background-color: lightblue;")

        # # 创建下拉菜单
        process_combo_box = QComboBox()
        # 向下拉菜单中添加选项
        # combo_box.addItem("选项1")
        # combo_box.addItem("选项2")
        # combo_box.addItem("选项3")
        # 创建按钮
        process_button = QPushButton("获取进程")
        capture_button = QPushButton("捕捉窗口")
        process_combo_box.setMaximumWidth(450)
        process_button.setMaximumWidth(100)  # 设置按钮的最大宽度为 100 像素
        capture_button.setMaximumWidth(100)

        # 定义按钮的点击事件,并向下拉菜单中添加选项
        def on_button_click():
            process_combo_box.clear()
            process = get_process()
            for temp_list in process:
                process_combo_box.addItem(temp_list)
                pass

        def button_clicked(combo_box):
            print(combo_box.currentText())
            get_screen_video(combo_box.currentText())
            # selected_item = combo_box.currentText()
            # result_label.setText(f"选中的内容是: {selected_item}")
        pass

        # 将按钮的点击事件与处理函数关联
        process_button.clicked.connect(on_button_click)
        capture_button.clicked.connect(partial(button_clicked, process_combo_box))

        # 添加控件进布局
        process_list_layout.addWidget(process_combo_box)
        process_list_layout.addWidget(process_button)
        process_list_layout.addWidget(capture_button)
        pass

    @staticmethod
    def init_other_layout(other_layout_widget, other_layout):
        """
        #其他布局视图
        :param other_layout_widget:其他布局视图背景部件
        :param other_layout:其他布局视图布局
        :return:
        """
        # 将子布局添加到子部件
        other_layout_widget.setLayout(other_layout)
        # 设置子布局的背景颜色
        other_layout_widget.setStyleSheet("background-color: white;")

        # # 创建下拉菜单
        label = QLabel("测试")
        button = QPushButton("测试")
        other_layout.addWidget(label)
        other_layout.addWidget(button)
        pass

    pass
