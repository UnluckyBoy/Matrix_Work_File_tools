# ---************************************************---
# @coding: utf-8
# @Time : 2024-07-24 13:12
# @Author : Matrix
# @File : StartMain.py
# @Software: PyCharm
# ---************************************************---
import argparse
from PIL import Image

ASCII_CHARS = "love "  # 定义字符集，字符集中的字符越多，生成的图片就越详细


def resize_image(image, new_width=64):
    """
    # 调整图片尺寸，保持长宽比，并设定新宽度 #
    :param image:原始图片
    :param new_width:新的图片宽高,默认64像素
    :return:
    """
    width, height = image.size
    ratio = height / width / 1.65  # 调整比例
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def gray_image(image):
    """
    # 将图片转换为灰度图 #
    :param image:
    :return:
    """
    grayscale_image = image.convert("L")
    return grayscale_image


def pixels_to_ascii(image):
    """
    # 将灰度图像素值映射为对应的ASCII字符 #
    :param image:
    :return:
    """
    # pixels = image.getdata()
    # ascii_str = ""
    # for pixel in pixels:
    #     ascii_str += ASCII_CHARS[pixel // 32]
    # return ascii_str
    pixels = image.getdata()
    ascii_str = ""
    ascii_len = len(ASCII_CHARS)
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel * ascii_len // 256]
    return ascii_str


def draw_image(image_path,output_file, new_width=64):
    """
    # 绘制图片 #
    :param output_file:
    :param image_path:图片路径
    :param new_width:图片宽高,默认64像素
    :return:
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, new_width)
    image = gray_image(image)
    ascii_str = pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    # 绘制图片逻辑 #
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i + img_width] + "\n"
    print(ascii_img)
    # 将ASCII字符图像写入文件
    with open(output_file, "w") as f:
        f.write(ascii_img)
    print(f"ASCII art written to {output_file}")


def main(args):
    image_path = "../Images/head_64x64.png"  # 替换为你图片的路径

    draw_image(image_path,args.outputPath)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filePath', type=str, default='./xxx/xxx', help='文件地址')
    parser.add_argument('--outputPath', type=str, default='../Images/out.txt', help='文件地址')
    # parser.add_argument('--filePath', type=str, required=True, help='文件地址')
    args = parser.parse_args()
    main(args)
