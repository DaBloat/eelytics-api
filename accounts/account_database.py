import sqlite3
from flask import g

DATABASE = 'database/accounts.db'
    
def get_bd():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

    
    