import sqlite3

conn = sqlite3.connect('health.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS preexisting_conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS family_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    age INTEGER,
    sex TEXT,
    bp_sys INTEGER,
    bp_dia INTEGER,
    hr INTEGER,
    temp REAL,
    pain INTEGER,
    symptoms TEXT,
    advice TEXT
)
''')

symptoms = [('Chest Pain',), ('Shortness of Breath',), ('Fever',), ('Cough',), ('Headache',), ('Dizziness',), ('Nausea',), ('Fainting',)]
conditions = [('Diabetes',), ('Heart Disease',), ('Asthma',)]
histories = [('Stroke',), ('Cancer',)]

conn.executemany('INSERT INTO symptoms (name) VALUES (?)', symptoms)
conn.executemany('INSERT INTO preexisting_conditions (name) VALUES (?)', conditions)
conn.executemany('INSERT INTO family_history (name) VALUES (?)', histories)

conn.commit()
conn.close()
