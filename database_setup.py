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

print("Creando tabla 'programas'...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS programas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        facultad TEXT NOT NULL,
        descripcion TEXT
    )
''')

cursor.execute("SELECT COUNT(*) FROM programas")
count = cursor.fetchone()[0]

if count == 0:
    print("Insertando datos de ejemplo en 'programas'...")
    programas_ejemplo = [
        ('Ingeniería de Sistemas', 'Facultad de Ingeniería', 'Formamos ingenieros capaces de diseñar, desarrollar y gestionar soluciones tecnológicas innovadoras.'),
        ('Administración de Empresas', 'Facultad de Ciencias Económicas', 'Preparamos líderes empresariales con visión estratégica y habilidades para la gestión eficiente de organizaciones.'),
        ('Comunicación Social', 'Facultad de Ciencias Sociales', 'Desarrollamos comunicadores con pensamiento crítico y dominio de diversas plataformas mediáticas.'),
        ('Contaduría Pública', 'Facultad de Ciencias Económicas', 'Profesionales capacitados en finanzas, auditoría y normatividad contable y tributaria.'),
        ('Diseño Gráfico', 'Facultad de Artes y Diseño', 'Creativos visuales con dominio de las herramientas y tendencias del diseño contemporáneo.'),
        ('Maestría en Innovación Educativa', 'Escuela de Posgrados', 'Programa para educadores que buscan transformar los procesos de enseñanza-aprendizaje.'),
        ('Maestría en Perder el tiempo', 'Escuela de Posgrados', 'Programa para refrijeradores y empujes haciendo uso de un equipo distribuidor, potenciado por un humano de fuerza.')
    ]
    cursor.executemany('INSERT INTO programas (nombre, facultad, descripcion) VALUES (?, ?, ?)', programas_ejemplo)
    print("Datos de programas insertados.")
else:
    print("La tabla 'programas' ya contiene datos.")

connection.commit()
connection.close()

print("Proceso de base de datos finalizado. 👍")