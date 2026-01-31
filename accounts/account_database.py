import sqlite3
from .accounts import Account
from flask import g
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, 'database', 'accounts.db')
    
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
def create_account_table():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                accounts (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    suffix TEXT,
                    profile_pic TEXT
                )
                """)
    db.commit()
    
def create_account(user:Account):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
                    INSERT INTO accounts(username, email, password, first_name, last_name, suffix, profile_pic)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    [user.username, user.email, user.password, user.first_name, user.last_name, user.suffix, user.profile_pic])
        db.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        
def read_all_accounts():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                SELECT username FROM accounts
                """)
    return [dict(i) for i in cur.fetchall()]

def get_account_cred(username):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                SELECT id, username, email, password FROM accounts WHERE username = ?
                """, [username])
    return cur.fetchone()

def update_account(id, update_dict:dict):
    db = get_db()
    cur = db.cursor()
    
    updates = [f'{key} = ?' for key in update_dict.keys()]
    clause = ", ".join(updates)
    update_values = list(update_dict.values())
    update_values.append(id)
    print(clause)
    print(update_values)
    cur.execute(f"""
                UPDATE accounts SET {clause}
                WHERE id = ?
                """, update_values)
    db.commit()
    
def delete_account(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                DELETE FROM accounts WHERE id = ?""",
                [id])
    db.commit()
        
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    
    with app.app_context():
        a = Account('Jason', 'Medina', 'IV', 'JMedina', 'jasonmedina.official@gmail.com', 'kunwarimaangasperoinde', 'image.jpg')
        print(a)
        # create_account(a)
        get_account_cred('Robert')
    

    
    