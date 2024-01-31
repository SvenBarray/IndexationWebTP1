import sqlite3

def insert_or_update_page(url, timestamp):
    "Fonction qui ajoute ou modifie une page à la database."
    conn = sqlite3.connect('database/crawler.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO pages (url, last_crawled) VALUES (?, ?)", 
              (url, timestamp))
    conn.commit()
    conn.close()