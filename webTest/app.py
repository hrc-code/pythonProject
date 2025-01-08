import os

from flask import Flask, request

from login_moblie import HutOpenApi

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()

account = os.getenv('account')
password = os.getenv('password')


@app.route("/grade")
def test():
    semester = request.args.get('semester')
    hutOpenApi = HutOpenApi()
    token = hutOpenApi.login(account, password)
    grade = hutOpenApi.get_grade(token, semester)
    return grade


@app.route("/grade/now")
def get_now_grade():
    semester = '2024-2025-1'
    hutOpenApi = HutOpenApi()
    token = hutOpenApi.login(account, password)
    grade = hutOpenApi.get_grade(token, semester)
    return grade


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32412, debug=False)
