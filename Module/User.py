import sqlite3

def getUser(id: int):
    conn = sqlite3.connect("User.db", isolation_level=None)
    c = conn.cursor()
    c.execute(f"SELECT * FROM User WHERE id={id}")
    n = c.fetchone()
    conn.close()
    return n