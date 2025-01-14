import os

from dotenv import load_dotenv

load_dotenv()

account = os.getenv('account')
print(account)

password = os.getenv('password')
print(password)



account = os.getenv('zhgd_account')
password = os.getenv('zhgd_password')

print(account)
print(password)

token_map = dict()

print(token_map.get('access_token')==None)