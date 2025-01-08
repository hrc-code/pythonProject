import requests


def get_courses():
    url = "https://kbhd.yixun.club/kebiao/term_kebiao"

    querystring = {"openid": "ou1BW44r0CTea9vaN0-9CAMX86RU", "semester": "2024-2025-1"}

    payload = {
        "openid": "ou1BW44r0CTea9vaN0-9CAMX86RU",
        "semester": "2024-2025-1"
    }
    headers = {

    }

    response = requests.post(url, data=payload, headers=headers, params=querystring)

    print(response.json())


def login():
    url = "https://kbhd.yixun.club/jiaowu/login_v3"

    querystring = {"sno": "333", "password": "333", "openid": "ou1BW44r0CTea9vaN0-9CAMX86RU", "sid": "1"}

    payload = {
        "sno": "333",
        "passwd": "333",
        "sid": 1,
        "openid": "ou1BW44r0CTea9vaN0-9CAMX86RU"
    }
    headers = {
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.json())


if __name__ == '__main__':
    login()
