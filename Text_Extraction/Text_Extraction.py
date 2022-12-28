# ---************************************************---
# @coding: utf-8
# @Time : 2022/12/28 0028 14:33
# @Author : Matrix
# @File : Text_Extraction.py
# @Software: PyCharm
# ---************************************************---
import argparse
import pytesseract
from PIL import Image

def Text_Extract(args):
    # image=Image.open("1.jpg")
    image = Image.open('./data/1.jpg')
    text = pytesseract.image_to_string(image, lang='chi_sim')  # 使用简体中文解析图片
    print(text)
    pass

def main(args):
    Text_Extract(args)
    pass

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--image_path',type=str,default='./data/01.jpg',help='文件地址')
    # parser.add_argument('--word_path',type=str,default='./data/demo.docx',help='word文件地址')
    args=parser.parse_args()
    main(args)