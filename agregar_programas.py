import sqlite3

nuevos_programas = [
    ('Psicología', 'Facultad de Ciencias Sociales', 'Estudio de la mente y el comportamiento humano para el bienestar individual y colectivo.'),
    ('Derecho', 'Facultad de Ciencias Jurídicas', 'Formación de abogados con sólidos principios éticos y conocimiento del marco legal.'),
    ('Arquitectura', 'Facultad de Artes y Diseño', 'Diseño y construcción de espacios que integran funcionalidad, estética y sostenibilidad.'),
    ('Medicina', 'Facultad de Ciencias de la Salud', 'Formación de profesionales de la salud con un enfoque científico y humanista.')
]

conn = sqlite3.connect('universidad.db')
cursor = conn.cursor()

print(f"Intentando añadir {len(nuevos_programas)} nuevos programas...")

for programa in nuevos_programas:
    nombre, facultad, descripcion = programa
    
    cursor.execute("SELECT COUNT(*) FROM programas WHERE nombre = ?", (nombre,))
    existe = cursor.fetchone()[0]
    
    if existe == 0:
        cursor.execute('INSERT INTO programas (nombre, facultad, descripcion) VALUES (?, ?, ?)', programa)
        print(f"✅ Programa '{nombre}' añadido exitosamente.")
    else:
        print(f"⚠️ El programa '{nombre}' ya existe en la base de datos. Se omitió.")
        
conn.commit()
conn.close()

print("\nProceso finalizado. ✅")