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


def build_ssr():
    ##SSR配置
    ##"$(get_ip):${shadowsocksport}:${shadowsockprotocol}:${shadowsockscipher}:${shadowsockobfs}:${shadowsockspwd}/?obfsparam="
    server_ip='153.92.4.237'
    server_port=(9889).__str__()
    protocol = 'origin'
    method = 'aes-256-cfb'
    obfs = 'plain'
    password=base64.urlsafe_b64encode(('back_use_vpn').encode(encoding="utf-8")).decode().replace('=','')#密码加密
    obfsparam=''

    ##SSR参数
    main_part = server_ip + ":" + server_port + ":" + protocol + ":" + method + ":" + obfs + ":" + password
    param_str = 'obfsparam=' + base64.urlsafe_b64encode(obfsparam.encode(encoding="utf- 8")).decode().replace('=', '')
    shareqrcode_str = "ssr://"+base64.urlsafe_b64encode((main_part + "/?" + param_str).encode(encoding="utf-8")).decode().replace('=','');
    print(main_part + "/?" + param_str)
    print(shareqrcode_str)

    pass


def main(args):
    build_ssr()
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./xxx/xxx', help='文件地址')
    args = parser.parse_args()
    main(args)
