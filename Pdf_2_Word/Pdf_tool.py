# ---************************************************---
# @coding: utf-8
# @Time : 2022/8/4 0004 20:21
# @Author : Matrix
# @File : Pdf_tool.py
# @Software: PyCharm
# ---************************************************---
import argparse
import os
from pdf2docx import Converter


def pdf_docx(pdf_file,word_path):
    """
    # pdf转word文件方法
    # pdf_file = './data/demo.pdf'
    # word_path = './data/demo.docx'
    :param pdf_file:
    :param word_path:
    :return:
    """
    #cv.convert(docx_file, start=0, end=5)#start是pdf转换的起始页,end是结束页;这里如果不传,则start和end的话默认就是从第一页转换到最后一页
    cv = Converter(pdf_file)
    cv.convert(word_path)
    cv.close()
    pass

def main(args):
    pdf_docx(args.pdf_path,args.word_path)
    pass

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--pdf_path',type=str,default='./data/123.pdf',help='pdf文件地址')
    parser.add_argument('--word_path',type=str,default='./data/123.docx',help='word文件地址')
    args=parser.parse_args()
    main(args)