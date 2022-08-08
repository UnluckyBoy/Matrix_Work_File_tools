# ---************************************************---
# @coding: utf-8
# @Time : 2022/8/8 0008 19:49
# @Author : Matrix
# @File : SplitStr.py
# @Software: PyCharm
# ---************************************************---
import os

def GetFile(path):
    """
    #读取文件并去掉符号
    :param path:
    :return:
    """
    strs=''
    result_str=''
    with open(path,'r',encoding='utf-8') as m_read:
        strs=m_read.read()
        pass
        str_list=strs.split(" ")
    print(str_list)

    for i in range(len(str_list)):
        result_str+=str_list[i]
        pass
    return result_str
    pass

def Save_Fiel_Txt(str_word,path):
    with open(path,'w+',encoding='utf-8') as m_write:
        m_write.write(str_word)
        pass
    print("保存完毕！___".format(path))
    pass

def main():
    read_path='./data/word.txt'
    save_path='./data/save_word.txt'
    str_result=GetFile(read_path)
    Save_Fiel_Txt(str_result,save_path)
    pass

if __name__=='__main__':
    main()