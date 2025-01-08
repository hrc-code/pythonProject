import requests
import ddddocr
import os
import time
from lxml import etree
import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

# 生成加密秘钥，根据账号密码和密钥对生成
def encode(data_str, user_account, user_password):  
    # 拆分data_str为scode和sxh  
    scode, sxh = data_str.split("#", 1)  # 限制分割次数为1  
  
    # 组合用户账号和密码  
    code = user_account + "%%%" + user_password  
  
    encoded = ""  
  
    # 遍历code的前20个字符（如果code长度小于20，则遍历整个code）  
    for i in range(min(len(code), 20)):  
        # 尝试从sxh中获取当前索引对应的长度（如果sxh中的字符不是数字，则使用0）  
        length = int(sxh[i]) if i < len(sxh) and sxh[i].isdigit() else 0  
  
        # 从scode中截取相应长度的字符串（确保不会超出scode的长度）  
        scode_part = scode[:length]  
        scode = scode[length:]  # 更新scode  
  
        # 拼接code的当前字符和scode的截取部分  
        encoded += code[i] + scode_part  
  
    # 如果code还有剩余部分，直接追加到encoded  
    if len(code) > 20:  
        encoded += code[20:]  
  
    return encoded  


# 1. 获取验证码 get：http://jwxt.hut.edu.cn/verifycode.servlet
# 2. 获取加密秘钥post：http://jwxt.hut.edu.cn/Logon.do?method=logon&flag=sess
#    响应格式为：g2d6oJrR5fj8623v7a8ObN4brhZ8352iQff73i4#33132131122213311312，由#前和#后两部分组成
#        g2d6oJrR5fj8623v7a8ObN4brhZ8352iQff73i4
#        33132131122213311312
#3. 验证码验证post：http://jwxt.hut.edu.cn/Logon.do?method=logon （302则成功，进行下一步，否则在xpath路径下的位置有错误信息：//*[@id="showMsg"]）
#    userAccount: 
#    userPassword: 
#    RANDOMCODE: 用户输入的验证码
#    encoded: 1qad86141155H5K3i4Hp00J0tH32K357l4%N%63d%lxut02tcx381Aj2f53321（账号密码生成的秘钥，根据上一步返回的密钥对生成的）

# baseUrl = "http://jwxt.hut.edu.cn"
baseUrl = "http://218.75.197.123:83"
# baseUrl = "http://csujwc.its.csu.edu.cn"
cookie_domain = "jwxt.hut.edu.cn"
# cookie_domain = "csujwc.its.csu.edu.cn"
img_path = "img/"
html_path = "html/"


if not os.path.exists(img_path):
    os.makedirs(img_path)
if not os.path.exists(html_path):
    os.makedirs(html_path)


# 获取登录session
def getsession(userAccount, userPassword) -> dict:
    start_time = time.time()

    sess = requests.session()
    # 1. 获取验证码
    resp = sess.get(baseUrl+'/verifycode.servlet', headers=headers)
    # 不存在img_path文件夹则创建
    imgname = img_path+userAccount+".jpg"
    with open(imgname, 'wb') as f:
        f.write(resp.content)
    # 打开验证码图片
    ocr = ddddocr.DdddOcr()
    with open(imgname, 'rb') as f:
        img_bytes = f.read()
    RANDOMCODE = ocr.classification(img_bytes)
    os.remove(imgname)

    # 2. 获取加密秘钥
    resp = sess.post(baseUrl+'/Logon.do?method=logon&flag=sess', headers=headers)
    data_str = resp.text

    # 3. 验证码验证
    encoded = encode(data_str, userAccount, userPassword)
    resp = sess.post(baseUrl+'/Logon.do?method=logon', data={
        'userAccount': userAccount,
        'userPassword': userPassword,
        'RANDOMCODE': RANDOMCODE,
        'encoded': encoded
    }, headers=headers)
    html_text = resp.text
    htmlname = html_path+userAccount+".html"
    with open(htmlname, 'w') as f:
        f.write(html_text)
    html = etree.HTML(html_text)
    errStr = ""
    showMsg = html.xpath('//*[@id="showMsg"]/text()')
    if len(showMsg) != 0:
        errStr = showMsg[0].strip()
    end_time = time.time()
    ts = "{:.2f}秒".format(end_time - start_time)
    if errStr != "":
        if "验证码错误" in errStr:
            os.remove(htmlname)
        txt = "{} cost: {}, account: {}, password: {}, error: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), ts, userAccount, userPassword, errStr)
        # logging.error("cost: %s, account: %s, password: %s, error: %s", ts, userAccount, userPassword, errStr)
        print(txt)
        end_time = time.time()
        return {"error": errStr, "cookie": ""}
    # 时间
    txt = "{} cost: {}, account: {}, password: {}, success".format(time.strftime("%Y-%m-%d %H:%M:%S"), ts, userAccount, userPassword)
    # logging.info("cost: %s, account: %s, password: %s, success", ts, userAccount, userPassword)
    print(txt)
    os.remove(htmlname)
    dd = sess.cookies.get_dict(cookie_domain)
    ret = ""
    for i in dd:
        ret = ret + (i + "=" + dd[i] + ";")
    # logging.info("Cookie"+ret)
    ret = "Cookie: " + ret
    return ret

