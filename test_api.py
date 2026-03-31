from accounts.account_database import *
from eels.eels_database import *
from flask import Flask
import os
import sqlite3

app = Flask(__name__)

with app.app_context():
    eel = EelDBManager(os.path.join('database', 'eelytics.db'))
    format_string()
    # eel.drop_table()
    # eel.create_table()
    # pop = EelData('date', 'time', 20, 'KUROKO', 'imgay')
    # eel.add_data(pop)
    # print(eel.show_data())
    # eel.delete_data(2)
    # print(eel.show_data())
    # create_account_table()
    # acc = Account('Kurt Russel', 'Villamor', '', 'DaBloat', 'kurtrusselvillamor1201@gmail.com', 'Potatolifeform', 'image.png')
    #acc = Account('Kurt', 'Villamor', '', 'DaBloatffs', 'kureetpop@gmail.com', 'Potatolifeform', 'image.png')
    # print(create_account(acc))
    # print(read_all_accounts())
    # print(get_account_cred('DaBloat'))
    # print(update_account(2, {'suffix':'II'}))
    # print(delete_account(2))
    # print(get_account_cred(''))
