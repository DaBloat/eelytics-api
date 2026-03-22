import sqlite3
from flask import g

class Account:
    def __init__(self, fn, ln, suf, usr, em, pas, pfp):
        self.first_name = fn
        self.last_name = ln
        self.suffix = suf
        self.username = usr
        self.email = em
        self.password = pas
        self.profile_pic = pfp
        
    def __str__(self):
        return f"Hi! I'm {self.first_name} {self.last_name} {self.suffix}, you can call me {self.username} and my email is {self.email} with hashed password of {self.password}"

class AccountManager:
    def __init__(self, db_path):
        self.db_path = db_path
    
    @property
    def connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_path, timeout=5)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA journal_mode=WAL;")
        return g.db
    
    def disconnect(self):
        db = g.pop('db', None)
        if db is not None:
            db.close()
    
    def create_table(self):
        db = self.connection
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
    
    def create_account(self, user:Account):
        db = self.connection
        cur = db.cursor()
        try:
            cur.execute("""
                        INSERT INTO accounts (username, email, password, first_name, last_name, suffix, profile_pic)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        [user.username, user.email, user.password, user.first_name, user.last_name, user.suffix, user.profile_pic])
            db.commit()
            return {'status': True, 'desc':'Account Created'}
        except sqlite3.Error as e:
            return {'status': False, 'desc': str(e)}
    
    def read_accounts(self):
        db = self.connection
        cur = db.cursor()
        cur.execute("""
                    SELECT id, username, email FROM accounts
                    """)
        return dict(cur.fetchall())
    
    def get_account_cred(self, username):
        db = self.connection
        cur = db.cursor()
        try:
            cur.execute("""
                        SELECT id, username, email, password FROM accounts WHERE username=?""",
                        [username])
            return dict(cur.fetchone())
        except TypeError:            
            return 0
        
    def update_account(self, id, update_dict:dict):
        db = self.connection
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
        
    def delete_account(self, id):
        db = self.connection
        cur = db.cursor()
        try:
            cur.execute("""
                        DELETE FROM accounts WHERE id=?""", 
                        [id])
            
            if cur.rowcount == 0:
                return {"status": False, "desc": f"No id={id} found"}
            
            db.commit()
            return {"status":True, "desc":"Account Deleted"}
        except sqlite3.Error as e:
            return {"status": False, 'desc': str(e)}