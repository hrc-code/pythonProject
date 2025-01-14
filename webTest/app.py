import os

from flask import Flask, request
import hut_zhgd
from login_moblie import HutOpenApi
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

account = os.getenv('account')
password = os.getenv('password')

token_map = dict()

hutOpenApi = HutOpenApi()


# 获取token
def get_token():
    token = token_map.get(account)
    if token is None:
        token = hutOpenApi.login(account, password)
        token_map[account] = token
    return token


@app.route("/grade")
def test():
    semester = request.args.get('semester')
    token = hutOpenApi.login(account, password)
    grade = hutOpenApi.get_grade(token, semester)
    return grade


@app.route("/v2/grade")
def get_grade():
    semester = request.args.get('semester')
    token = get_token()
    grade = hutOpenApi.get_grade(token, semester)
    return grade


@app.route("/grade/now")
def get_now_grade():
    semester = '2024-2025-1'
    token = get_token()
    grade = hutOpenApi.get_grade(token, semester)
    return grade


@app.route("/v2/grade/now")
def get_now_grade2():
    semester = '2024-2025-1'
    token = get_token()
    grade = hutOpenApi.get_grade(token, semester)
    return grade

# 查询电费

@app.route("/getElectricity")
def get_electricity():
    return  hut_zhgd.get_electricity()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32412, debug=False)
