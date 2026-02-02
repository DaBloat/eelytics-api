import sqlite3
from .accounts import Account
from flask import g
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, 'database', 'accounts.db')
    
def get_db():
    """Connect to the Database and set it to be accessible as a Dictionary
    if it not in the flask "bucket"

    Returns:
        sq3lite.Connection: The Database connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
def create_account_table():
    """Create table, thats it
    
    Returns:
        dict: this one is for the API conditionals, response
    """
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
    return True
    
def create_account(user:Account):
    """
    Creates an account using the Account Object.
    returns a response in dict
    
    :param user: Description
    :type user: Account
    :return: Description
    :rtype: dict[str, Any]
    """
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
                    INSERT INTO accounts(username, email, password, first_name, last_name, suffix, profile_pic)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    [user.username, user.email, user.password, user.first_name, user.last_name, user.suffix, user.profile_pic])
        db.commit()
        return {'status':True, 'desc':'Account Created'}
    except sqlite3.Error as e:
        return {'status':False, 'desc': str(e)}
        
def read_all_accounts():
    '''Returns a list of dictionaries for usernames'''
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                SELECT id, username FROM accounts
                """)
    return cur.fetchall()

def read_profile_account():
    pass

def get_account_cred(username):
    '''
    returns a Row object(dict) of user credentials
    
    :param username: accepts the username of the account
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                SELECT id, username, email, password FROM accounts WHERE username = ?
                """, [username])
    return cur.fetchone()

def update_account(id, update_dict:dict):
    '''
    Logic for updating your account in the database
    
    :param id: Account ID given by the Database
    :param update_dict: a Dict of things you want to update
    :type update_dict: dict
    '''
    db = get_db()
    cur = db.cursor()
    try: 
        updates = [f'{key} = ?' for key in update_dict.keys()]
        clause = ", ".join(updates)
        update_values = list(update_dict.values())
        update_values.append(id)
        cur.execute(f"""
                    UPDATE accounts SET {clause}
                    WHERE id = ?
                    """, update_values)

        if cur.rowcount == 0:
            return {'status':False, 'desc': f'no id={id}'}
        
        db.commit()
        return {'status':True, 'desc':'Account Updated'}
    except sqlite3.Error as e:
        return {'status':False, 'desc': str(e)}
    
def delete_account(id):
    '''
    deleting the account using the account's id
    
    :param id: Account ID given by the Database
    '''
    db = get_db()
    cur = db.cursor()
    cur.execute("""
                DELETE FROM accounts WHERE id = ?""",
                [id])
    if cur.rowcount == 0:
        return {'status':False, 'desc': f'no id={id}'}

    db.commit()
    return {'status':True, 'desc':'Account Deleted'}