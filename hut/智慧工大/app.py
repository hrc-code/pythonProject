import os

import requests
from dotenv import load_dotenv

load_dotenv()


def login(username, password):
    session = requests.session()

    url = "https://mycas.hut.edu.cn/token/password/passwordLogin"

    querystring = {"username": username, "password": password, "appId": "com.supwisdom.hut", "geo": "",
                   "deviceId": "Z20bPxiMxVYDAJikw0SeHZ5M", "osType": "android",
                   "clientId": "d58daac6b3efd99d21e57ad63c7a619c", "mfaState": ""}

    headers = {
        "User-Agent": "SWSuperApp/1.1.3(XiaomimondrianRedmi7.1.2)",
        "Content-Length": "0",
        "Host": "mycas.hut.edu.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    response = session.post(url, headers=headers, params=querystring)
    id_token = response.json()['data']['idToken']
    print(id_token)

    session.cookies.set('userToken', id_token)

    get_electricity(session)


def get_electricity(session):

    url = "http://v8mobile.hut.edu.cn/channel/queryRoomDetail"

    querystring = {
        "openid": "FD868A4AFF8878A33B4BC5443A6C02BBD4317C134B542FE73C5C7FC5F24D0CF2E113BDDEC388C0038475E2EB8243D087"}

    payload = {
        "areaid": "44517536-4",
        "buildingid": "25",
        "factorycode": "N002",
        "roomid": "4D9BB38D13354D32A75F75D3326696C1"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Host": "v8mobile.hut.edu.cn"
    }

    response = session.post(url, json=payload, headers=headers, params=querystring)

    print(response.text)

if __name__ == '__main__':
    account = os.getenv('account')
    password = os.getenv('password')
    login(account, password)
