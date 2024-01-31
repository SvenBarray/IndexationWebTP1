import sqlite3

def create_database():
    "Fonction qui permet la création de la database des pages crawlées."
    conn = sqlite3.connect('database/crawler.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pages
                 (url TEXT PRIMARY KEY, last_crawled TIMESTAMP)''')
    conn.commit()
    conn.close()

create_database()