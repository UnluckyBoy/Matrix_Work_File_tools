# ---************************************************---
# @coding: utf-8
# @Time : 2023/5/2 0002 21:03
# @Author : Matrix
# @File : start_build.py
# @Software: PyCharm
# ---************************************************---
import argparse
import base64
import qrcode
import matplotlib.pyplot as plt
from PIL import Image


def build_ssr():
    ##SSR配置
    ##"$(get_ip):${shadowsocksport}:${shadowsockprotocol}:${shadowsockscipher}:${shadowsockobfs}:${shadowsockspwd}/?obfsparam="
    server_ip='185.28.23.244'
    server_port=(9889).__str__()
    protocol = 'origin'
    method = 'aes-256-cfb'
    obfs = 'plain'
    password=base64.urlsafe_b64encode(('beiyong_vpn_port').encode(encoding="utf-8")).decode().replace('=','')#密码加密
    obfsparam=''

    ##SSR参数
    main_part = server_ip + ":" + server_port + ":" + protocol + ":" + method + ":" + obfs + ":" + password
    param_str = 'obfsparam=' + base64.urlsafe_b64encode(obfsparam.encode(encoding="utf- 8")).decode().replace('=', '')
    shareqrcode_str = "ssr://"+base64.urlsafe_b64encode((main_part + "/?" + param_str).encode(encoding="utf-8")).decode().replace('=','');
    print(main_part + "/?" + param_str)
    print(shareqrcode_str)

    ##生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,)
    # 添加数据
    qr.add_data(shareqrcode_str)
    # 填充数据
    qr.make(fit=True)
    # 生成图片
    img = qr.make_image(fill_color="green", back_color="white")

    # 添加logo，打开logo照片
    icon = Image.open("./data/head_icon.jpg")
    # 获取图片的宽高
    img_w, img_h = img.size
    # 参数设置logo的大小
    factor = 6
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    # 重新设置logo的尺寸
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    # 得到画图的x，y坐标，居中显示
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    # 黏贴logo照
    img.paste(icon, (w, h), mask=None)
    # 终端显示图片
    plt.imshow(img)
    plt.show()

    pass


def main(args):
    build_ssr()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
