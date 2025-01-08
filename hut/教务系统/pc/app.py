import os

import ddddocr
import requests
import re

import js
from dotenv import load_dotenv

load_dotenv()

ocr = ddddocr.DdddOcr()

cookie_domain = "jwxt.hut.edu.cn"




# pc登录流程 先拿到盐,对密码加密,然后获取验证码，在登录

# 拿盐
def get_salt(session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    url = "http://jwxt.hut.edu.cn/jsxsd/"
    response = session.get(url, headers=headers, verify=False)
    print(re.findall("var scode = \"(.*?)\";", response.text))
    scode = re.findall("var scode = \"(.*?)\";", response.text)[0]
    print(re.findall("var sxh = \"(.*?)\";", response.text))
    sxh = re.findall("var sxh = \"(.*?)\";", response.text)[0]

    return scode, sxh


# 获取验证码

def get_verify_code(session: requests.Session):
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://jwxt.hut.edu.cn/jsxsd/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    url = "http://jwxt.hut.edu.cn/jsxsd/verifycode.servlet"
    params = {
        "t": "0.7150063561951752"
    }
    response = session.get(url, headers=headers, params=params, verify=False)
    # 将二进制保存为本地图片
    # binary_image_data 是包含图像二进制数据的字节对象

    # 指定要保存的图片路径和名称
    imgname = './verify_code.jpg'
    # 打开文件并写入二进制数据
    with open(imgname, 'wb') as f:
        f.write(response.content)
    # 打开验证码图片
    with open(imgname, 'rb') as f:
        img_bytes = f.read()
    RANDOMCODE = ocr.classification(img_bytes)
    # os.remove(imgname)
    print(RANDOMCODE)
    return RANDOMCODE


# 登录

def login(userAccount, userPassword):
    session = requests.Session()

    # 获取盐
    scode, sxh = get_salt(session)
    print(scode)
    print(sxh)
    # 加密
    login_js = js.jsx('login-pc.js')
    encode = login_js.call('submitForm1', userAccount, userPassword, scode, sxh)
    print('==========encode=========')
    # 获取验证码
    RANDOMCODE = get_verify_code(session)

    url = "http://jwxt.hut.edu.cn/jsxsd/xk/LoginToXk"

    payload = {
        "loginMethod": "LoginToXk",
        "userlanguage": "0",
        "userAccount": userAccount,
        "userPassword": "",
        "RANDOMCODE": RANDOMCODE,
        "encoded": encode
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://jwxt.hut.edu.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://jwxt.hut.edu.cn/jsxsd/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    response = session.post(url, data=payload, headers=headers)

    cookie = session.cookies.get_dict(cookie_domain)
    print(cookie)
    return cookie
    # ret = ""
    # for i in dd:
    #     ret = ret + (i + "=" + dd[i] + ";")
    # ret = "Cookie: " + ret
    # print(ret)


def get_grade(cookie):
    import requests

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://jwxt.hut.edu.cn/jsxsd/kscj/cjcx_frm",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = cookie
    url = "http://jwxt.hut.edu.cn/jsxsd/kscj/cjcx_list"
    params = {
        "pageNum": "1",
        "pageSize": "20",
        "kksj": "",
        "kcxz": "",
        "kcsx": "",
        "kcmc": "",
        "xsfs": "all",
        "sfxsbcxq": "1"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)

    print(response.text)


if __name__ == '__main__':
    account = os.getenv('account')
    password = os.getenv('password')
    cookie = login(account, password)
    get_grade(cookie)
