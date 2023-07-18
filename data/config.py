from pathlib import Path

def set_data():
    SECRET_KEY = b'r9\xee*\x13\x96\xf7L\x9c8\x98\x8aM\xfb\x8e~'
    DATABASE = Path().resolve() / 'data/users.db'
    
set_data()