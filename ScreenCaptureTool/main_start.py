# ---************************************************---
# @coding: utf-8
# @Time : 2023/10/10 0010 14:25
# @Author : Matrix
# @File : main_start.py
# @Software: PyCharm
# ---************************************************---
import argparse

from ScreenCaptureTool.pidTool.get_Pid import *
from ScreenCaptureTool.screenTool.screenTools import *
from ScreenCaptureTool.ui.main_ui import *
from ScreenCaptureTool.ui.main_window import ScreenRecorderMainUi


def main(args):
    # get_screen_video()
    app = QApplication(sys.argv)
    # window = CaptureWindow()
    # window.setFixedSize(1920, 1080)  # 设置窗口的宽度为 1920 像素，高度为 1080 像素
    window = ScreenRecorderMainUi(1920,1080)
    window.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
