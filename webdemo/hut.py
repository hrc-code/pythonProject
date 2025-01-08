import base64

import requests

cookie_domain = "jwxt.hut.edu.cn"


# 无验证码登录
def login(username, password):
    ss = requests.Session()
    print("Logging in...")
    # 先base64编码
    # 将字符串转换为字节对象
    username_bytes = username.encode('utf-8')
    password_bytes = password.encode('utf-8')

    # 对字节对象进行 base64 编码
    encoded_username = base64.b64encode(username_bytes)
    encoded_password = base64.b64encode(password_bytes)

    # 将编码后的字节对象转换为字符串，并拼接
    encode = encoded_username.decode('utf-8') + '%%%' + encoded_password.decode('utf-8')
    # print(encode)

    url = "http://jwxt.hut.edu.cn/jsxsd/xk/LoginToXk"
    data = "loginMethod=LoginToXk&userlanguage=0&userAccount=" + username + "&userPassword=&encoded=" + encode

    # 开始登录
    ss.post(url=url, data=data)

    dd = ss.cookies.get_dict(cookie_domain)
    ret = ""
    for i in dd:
        ret = ret + (i + "=" + dd[i] + ";")
    ret = "Cookie: " + ret
    print(ret)
