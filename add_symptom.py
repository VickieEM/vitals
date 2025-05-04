import sqlite3

# Connect to the database
conn = sqlite3.connect('health.db')
c = conn.cursor()

# Insert "Back Pain" symptom
c.execute('INSERT INTO symptoms (name) VALUES (?)', ('Back Pain',))

# Save changes and close
conn.commit()
conn.close()

print("Back Pain added successfully!")
