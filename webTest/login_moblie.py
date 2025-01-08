import base64
import os

from js import jsx
import requests

from dotenv import load_dotenv

load_dotenv()

account = os.getenv('account')
password = os.getenv('password')


class HutOpenApi:

    def get_grade_cet_4_6(self, token):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-length": "0",
            "origin": "https://jwxtsj.hut.edu.cn",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://jwxtsj.hut.edu.cn/sjd/",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "token": token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        url = "https://jwxtsj.hut.edu.cn/njwhd/student/socialTestScores"
        params = {
            "examName": ""
        }
        response = requests.post(url, headers=headers, params=params)
        json_response = response.json()
        cet_6 = json_response["data"][0]['overallResult']
        cet_4 = json_response["data"][1]['overallResult']
        return cet_6, cet_4

    # 获取成绩
    def get_grade(serf, token, semester):
        # semester 2023-2024-2
        url = "https://jwxtsj.hut.edu.cn/njwhd/student/termGPA"

        querystring = {"semester": semester, "type": "1"}

        headers = {
            "accept": "application/json, text/plain, */*",
            "token": token,
        }

        response = requests.post(url, headers=headers, params=querystring)

        json_response = response.json()

        code = json_response["code"]
        if (code == '0'):
            token = serf.login(account, password)
            return serf.get_grade(token, semester)
        
        print(json_response)
        return json_response

    def login(this, username, password):
        # 加密
        txt = "\"" + password + "\""
        key = os.getenv("hut_mobile_secret_key")
        aes_pwd = jsx('aes-js.js').call('encryptAES_ECB', txt, key)
        print('===========encryptAES_ECB===============')
        print(aes_pwd)
        # base64
        base64_pwd = base64.b64encode(aes_pwd.encode('utf-8')).decode('utf-8')
        print('==========base64_pwd=========')
        print(base64_pwd)
        encrypted_pwd = base64_pwd

        headers = {
            "^accept": "application/json, text/plain, */*^",
            "^accept-language": "zh-CN,zh;q=0.9^",
        }
        url = "https://jwxtsj.hut.edu.cn/njwhd/login"
        params = {
            "userNo": username,
            "pwd": encrypted_pwd
        }
        response = requests.post(url, headers=headers, params=params)
        # print(response.text)
        token = response.json()['data']['token']
        print('==========token========')
        print(token)
        return token


if __name__ == '__main__':
    hutOpenApi = HutOpenApi()
    # token = hutOpenApi.login(account, password)
    hutOpenApi.get_grade('token', '2024-2025-1')

# cet_6, cet_4 = get_grade_cet_4_6(token)
# print("=======六级================四级============")
# print(cet_6, cet_4)
