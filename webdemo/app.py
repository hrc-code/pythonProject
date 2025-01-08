

from flask import Flask, request
import logging


from views import getsession

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


@app.route('/login')
def hello_world():
    # 获取username和password
    user_account = request.args.get('username')
    user_password = request.args.get('password')
    # 获取登录session
    sess = getsession(user_account, user_password)
    return sess


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8018)

