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
        str_list=strs.split("、")
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
    str_result='一乙二十丁厂七卜人入八九几儿了力乃刀又三于干亏士工土才寸下大丈与万上小口巾山千乞川亿个勺久凡及' \
               '夕丸么广亡门义之尸弓己已子卫也女飞刃习叉马乡丰王井开夫天无元专云扎艺木五支厅不太犬区历尤友匹车' \
               '巨牙屯比互切瓦止少日中冈贝内水见午牛手毛气升长仁什片仆化仇币仍仅斤爪反介父从今凶分乏公仓月氏勿' \
               '欠风丹匀乌凤勾文六方火为斗忆订计户认心尺引丑巴孔队办以允予劝双书幻'
    str=GetFile(read_path)
    str_result+=str
    Save_Fiel_Txt(str_result,save_path)
    pass

if __name__=='__main__':
    main()