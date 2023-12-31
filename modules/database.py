import sqlite3

from flask import current_app, g

def get_db(data_base):
    print("get_db")
    if 'db' not in g:
        g.db = sqlite3.connect(data_base)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
 