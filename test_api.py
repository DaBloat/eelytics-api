from accounts.account_database import *
from accounts.accounts import Account
from flask import Flask

app = Flask(__name__)

with app.app_context():
    acc = Account('Kurt Russel', 'Villamor', '', 'DaBloat', 'kurtrusselvillamor1201@gmail.com', 'Potatolifeform', 'image.png')
    print(create_account(acc))
    # print(read_all_accounts())
    # print(get_account_cred('DaBloat'))
    # print(update_account(2, {'suffix':'II'}))
    # print(delete_account(2))
