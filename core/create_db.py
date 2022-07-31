import sqlite3 as sl 
from db import cur

con = sl.connect('ping.db')

cur = con.cursor()

cur.execute('''
    CREATE TABLE user(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE services(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        period INTEGER NOT NULL,
        url TEXT,
        port INTEGER,
        user_created INTEGER,
        FOREIGN KEY(user_created) REFERENCES user(id)
    )
''')

cur.execute('''
    CREATE TABLE tasks_runner(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        next_check INT NOT NULL,
        service_id INTEGER,
        notify INT NOT NULL,
        FOREIGN KEY(service_id) REFERENCES services(id)
    )
''')