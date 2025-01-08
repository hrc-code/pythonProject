import os

from dotenv import load_dotenv

load_dotenv()

account = os.getenv('account')
print(account)

password = os.getenv('password')
print(password)

key = os.getenv("hut_mobile_secret_key")
print(key)