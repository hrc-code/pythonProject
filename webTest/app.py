import os

from flask import Flask, request
import hut_zhgd
from login_moblie import HutOpenApi
from dotenv import load_dotenv
import logging
load_dotenv()

app = Flask(__name__)

account = os.getenv('account')
password = os.getenv('password')


hutOpenApi = HutOpenApi()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('app_loggerr')




# @app.route("/grade")
# def test():
#     semester = request.args.get('semester')
#     token = hutOpenApi.login(account, password)
#     grade = hutOpenApi.get_grade(token, semester)
#     return grade


@app.route("/grade")
def get_grade():
    semester = request.args.get('semester')
    grade = hutOpenApi.get_grade (semester)
    logger.info("返回结果:%s",grade)
    return grade


@app.route("/grade/now")
def get_now_grade():
    semester = '2024-2025-1'
    grade = hutOpenApi.get_grade( semester)
    logger.info("返回结果:%s",grade)
    return grade


# @app.route("/v2/grade/now")
# def get_now_grade2():
#     semester = '2024-2025-1'
#     token = get_token()
#     grade = hutOpenApi.get_grade(token, semester)
#     return grade

# 查询电费

@app.route("/getElectricity")
def get_electricity():
    return  hut_zhgd.get_electricity()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32412, debug=False)
