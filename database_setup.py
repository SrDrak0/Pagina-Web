import sqlite3


connection = sqlite3.connect('universidad.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        carrera TEXT NOT NULL
    )
''')

print("Base de datos y tabla 'estudiantes' creadas exitosamente. 👍")

connection.commit()
connection.close()