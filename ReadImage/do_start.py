# ---************************************************---
# @coding: utf-8
# @Time : 2023/7/25 0025 21:27
# @Author : Matrix
# @File : do_start.py
# @Software: PyCharm
# ---************************************************---
import argparse
import cv2
import numpy as np
import requests
from uiautomator import Device
import unittest
import os
import time


def find_button_in_image(main_image_path, sub_image_path):
    """
    :param sub_image_path: # 主图像的路径
    :param main_image_path: # 子图像（截取部分）的路径
    :return:
    """
    # 读取主图像和子图像，并转换为灰度图像
    # main_image = cv2.imread(main_image_path)
    # sub_image = cv2.imread(sub_image_path)
    # sub_image_gray = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
    main_image = cv2.imread(main_image_path, cv2.IMREAD_GRAYSCALE)
    sub_image = cv2.imread(sub_image_path, cv2.IMREAD_GRAYSCALE)

    # 使用模板匹配算法
    result = cv2.matchTemplate(main_image, sub_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 设置匹配阈值，可以根据需求调整
    loc = np.where(result >= threshold)

    # 在主图像中找到匹配位置并用红框标出
    h, w = sub_image.shape
    for pt in zip(*loc[::-1]):
        top_left = pt
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(main_image, top_left, bottom_right, (0, 0, 255), 2)

    # 显示结果图像
    cv2.imshow('Result', main_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(args):
    find_button_in_image(args.main_image, args.sub_image)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--main_image', type=str, default='./data/2333.jpg', help='主图像')
    parser.add_argument('--sub_image', type=str, default='./data/23.png', help='子图像')
    args = parser.parse_args()
    main(args)
