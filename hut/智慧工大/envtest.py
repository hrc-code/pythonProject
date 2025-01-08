import os

from dotenv import load_dotenv

load_dotenv()

account = os.getenv('account')
print(account)

password = os.getenv('password')
print(password)
