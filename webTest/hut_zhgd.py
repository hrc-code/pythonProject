import os

import requests
from dotenv import load_dotenv

load_dotenv()
account = os.getenv('zhgd_account')
password = os.getenv('zhgd_password')

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
    print('id_token: '+id_token)

    return id_token




token_map = dict()

def get_token():
    token =  token_map.get('account')
    if token is None:
        token = login(account, password)
        token_map['account'] = token
    return token

def remove_token():
     token_map.pop('account','key not found')
# 查电费1

def get_electricity_1(userToken):
    session = requests.session()
    url = "https://v8mobile.hut.edu.cn/zdRedirect/toSingleMenu"

    params = {
        'code': "openElePay",
        'X-Id-Token': userToken
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 14; 23013RK75C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36 SuperApp",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Android WebView\";v=\"126\"",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'Upgrade-Insecure-Requests': "1",
        'X-Requested-With': "com.supwisdom.hut",
        'Sec-Fetch-Site': "none",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Sec-Fetch-Dest': "document",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': userToken
    }

    session.get(url, params=params, headers=headers)

    result = get_electricity_2(session)
    return result

def get_electricity_2( session):
    import json


    userToken = "eyJhbGciOiJSUzUxMiJ9.eyJBVFRSX3VzZXJObyI6IjIyNDA4MDAwNTExIiwic3ViIjoiMjI0MDgwMDA1MTEiLCJpc3MiOiJteWNhcy5odXQuZWR1LmNuIiwiZGV2aWNlSWQiOiJZL0JuOEw5SW1CUURBQVlQK3Y5ZUlXcksiLCJBVFRSX2lkZW50aXR5VHlwZUlkIjoiMDM3MTQ0YTA2YTBjMTFlZGI4MDM2MjZhOGNlMzI2MjkiLCJBVFRSX2FjY291bnRJZCI6IjhiN2IxNTEwOGI0ZjExZWQxNmJkOTYyYWFiYzM3NGNkIiwiQVRUUl91c2VySWQiOiI4YjZkMzI2MDhiNGYxMWVkMTZiZDk2MmFhYmMzNzRjZCIsIkFUVFJfaWRlbnRpdHlUeXBlQ29kZSI6IlMwMiIsIkFUVFJfaWRlbnRpdHlUeXBlTmFtZSI6IuWtpueUnyIsIkFUVFJfb3JnYW5pemF0aW9uTmFtZSI6IueJqeiBlOe9kTIyMDIiLCJBVFRSX3VzZXJOYW1lIjoi6buE5pel5oiQIiwiZXhwIjoxNzM5Mzg1MDU2LCJBVFRSX29yZ2FuaXphdGlvbklkIjoiMDVfMjAyMjA4NTAwMiIsImlhdCI6MTczNjc5MzA1NiwianRpIjoiSWQtVG9rZW4tazBBcU9iY0VZZmVmc3hNMSIsInJlcSI6ImNvbS5zdXB3aXNkb20uaHV0IiwiQVRUUl9vcmdhbml6YXRpb25Db2RlIjoiMDVfMjAyMjA4NTAwMiJ9.QxHmw4a4lPci3HId8SdkOQND6EY-8g7kgwbUcea3FfwKgg_ColX2jgCuSRRtHmXsW6xRA_w7kBqXkfz-Rs_dV7XA12UVMrsNj5QxDEFxjCbJ4i9DVAAuYGsNtrOC6CP_OM0IwiRZRHFLlFCS0XR0yGxoBpzDr2sqrZ7FuBXN0dg1B0AnE2wm00Tw57yH2eMNB6DRaATwz8MlvtoNO4EnutuO2FVZpIkdG1rCYj5a8U1XOv4pqpz-RVOTDOhBs8Uvpg0nYy-gsObzqKBCOMKQA8IVP32MYwva4YgEnWlzsFK2mEBaLEopAGVZkMCelopp_P4EBoWQmtbg9r6l60xX7A"
    url = "https://v8mobile.hut.edu.cn/channel/queryRoomDetail"

    session.cookies.set('userToken',userToken)

    params = {
        'openid': "FD868A4AFF8878A33B4BC5443A6C02BBD4317C134B542FE73C5C7FC5F24D0CF2E113BDDEC388C0038475E2EB8243D087"
    }

    payload = {
        "areaid": "44517536-4",
        "buildingid": "25",
        "factorycode": "N002",
        "roomid": "4D9BB38D13354D32A75F75D3326696C1"
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 14; 23013RK75C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36 SuperApp",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Android WebView\";v=\"126\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://v8mobile.hut.edu.cn",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://v8mobile.hut.edu.cn/elepay/openElePay?openid=FD868A4AFF8878A33B4BC5443A6C02BBD4317C134B542FE73C5C7FC5F24D0CF2E113BDDEC388C0038475E2EB8243D087",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    response = session.post(url, params=params, data=json.dumps(payload), headers=headers)

    print('电费查询结果')
    print(response.json())
    return  response.json()

def do_get_electricity():
    token = get_token()
    result = get_electricity_1(token)
    return result

def get_electricity():
    result = do_get_electricity()
    print('get_electricity')
    print(result)
    count = 0
    if (result['success'] == False):
        while(count < 3):
            remove_token()
            result = do_get_electricity()
            time = count + 1
            print('第' + str(time)+'次重试'+'\n'+str(result))
            count += 1

    return result




if __name__ == '__main__':
    # remove_token()
    get_electricity()

    # login(account, password)
