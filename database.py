import sqlite3


database=sqlite3.connect('translator_history')
cursor=database.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER,
    first_lang TEXT,
    second_lang TEXT,
    translated_text TEXT
    );
''')


database.commit()
database.close()