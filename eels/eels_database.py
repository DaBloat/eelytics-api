import sqlite3
import re
from flask import g
import datetime


class EelData:
    def __init__(self, date, time, size, group, img):
        self.date = date
        self.time = time
        self.size = size
        self.group = group
        self.img = img
    
    def show(self):
        return f"{self.date} @ {self.time}, Found a {self.group} with {self.size} inches!"
        

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
                        time TEXT NOT NULL,
                        size REAL NOT NULL,
                        data_group TEXT NOT NULL,
                        img TEXT
                    )
                    """)
        db.commit()
        return True
    
    def drop_table(self):
        db = self.connection
        cur = db.cursor()
        cur.execute("""
                    DROP TABLE IF EXISTS eelsdb
                    """)
        db.commit()
        return True
        
    
    def add_data(self, eels:EelData):
        db = self.connection
        cur = db.cursor()
        try:
            cur.execute("""
                        INSERT INTO eelsdb (date, time, size, data_group, img)
                        VALUES (?, ?, ?, ?, ?)""", 
                        [eels.date, eels.time, eels.size, eels.group, eels.img])
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
        
    def get_average(self, group):
        db = self.connection
        cur = db.cursor()
        cur.execute(f"""
                    SELECT size FROM eelsdb WHERE data_group='{group}'
                    """)
        row = cur.fetchall()
        return [dict(item) for item in row]

def format_string(log_str):
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")
    pattern = r"(?P<time>\d{2}:\d{2}:\d{2}) - Detected : (?P<inches>[\d.]+) in as (?P<group>ELVER|KUROKO|TABLE)"
    available = re.search(pattern, log_str)
    if available:
        time = available.group('time')
        inches = available.group('inches')
        group = available.group('group')
        return date, time, inches, group
