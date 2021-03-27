import sqlite3 as sl


class dbinitClass:
    def __init__(self):
        con = sl.connect('bd.db')
        cur = con.cursor()
        cur.execute("""
                 CREATE TABLE IF NOT EXISTS users(
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            action TEXT
                        );
                """)

        con.commit()
