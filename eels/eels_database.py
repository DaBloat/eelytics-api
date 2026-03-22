import sqlite3
from flask import g


class EelData:
    def __init__(self, date, size, group, img):
        self.date = date
        self.size = size
        self.group = group
        self.img = img
        

class EelDBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        
    @property
    def connection(self):
        if "db" not in g:
            g.db = sqlite3.connect(self.db_path, timeout=5)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA journal_mode=WAL;")
        return g.db
    
    def disconnect(self):
        db = g.pop("db", None)
        if db is not None:
            db.close()
            
    def create_table(self):
        db = self.connection
        cur = db.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS
                    eelsdb (
                        id INTEGER PRIMARY KEY,
                        date TEXT NOT NULL,
                        size REAL NOT NULL,
                        data_group TEXT NOT NULL,
                        img TEXT
                    )
                    """)
        db.commit()
        return True
    
    def add_data(self, eels:EelData):
        db = self.connection
        cur = db.cursor()
        try:
            cur.execute("""
                        INSERT INTO eelsdb (date, size, data_group, img)
                        VALUES (?, ?, ?, ?)""", 
                        [eels.date, eels.size, eels.group, eels.img])
            db.commit()
            return {'status': True, 'desc':'Eels Data Created'}
        except sqlite3.Error as e:
            return {'status': False, 'desc': str(e)}
        
    def show_data(self):
        db = self.connection
        cur = db.cursor()
        cur.execute("""
                    SELECT * FROM eelsdb""")
        row = cur.fetchall()
        return [dict(item) for item in row]
    
    def delete_data(self, id):
        db = self.connection
        cur = db.cursor()
        try:
            cur.execute("""
                        DELETE FROM eelsdb WHERE id=?""", 
                        [id])
            
            if cur.rowcount == 0:
                return {"status": False, "desc": f"No id={id} found"}
            
            db.commit()
            return {"status":True, "desc":"Eels Data Deleted"}
        except sqlite3.Error as e:
            return {"status": False, 'desc': str(e)}
        