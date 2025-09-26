from flask import Flask, render_template, url_for, request, redirect
import sqlite3 

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/mision")
def mision():
    return render_template('mision.html')

@app.route("/vision")
def vision():
    return render_template('vision.html')

@app.route("/programas")
def programas():

    conn = sqlite3.connect('universidad.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM programas ORDER BY facultad, nombre')
    
    lista_de_programas = cursor.fetchall()
    
    conn.close()

    return render_template('programas.html', programas=lista_de_programas)

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        carrera = request.form['carrera']

       
        if not nombre or not apellido or not email or not carrera:
            error_msg = "Todos los campos son obligatorios. Por favor, inténtelo de nuevo."
           
            return render_template('registro.html', error=error_msg)
        
        try:
           
            conn = sqlite3.connect('universidad.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO estudiantes (nombre, apellido, email, carrera) VALUES (?, ?, ?, ?)',
                           (nombre, apellido, email, carrera))
            conn.commit()
            conn.close()
           
            return redirect(url_for('exito'))

        except sqlite3.IntegrityError:
         
            error_msg = "El correo electrónico ya está registrado. Use uno diferente."
            return render_template('registro.html', error=error_msg)

    
    return render_template('registro.html')


@app.route("/exito")
def exito():
    return render_template('exito.html')


@app.route('/programas/agregar', methods=['GET', 'POST'])
def agregar_programa():
    if request.method == 'POST':
        nombre = request.form['nombre']
        facultad = request.form['facultad']
        descripcion = request.form['descripcion']

        if nombre and facultad: 
            conn = sqlite3.connect('universidad.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO programas (nombre, facultad, descripcion) VALUES (?, ?, ?)',
                           (nombre, facultad, descripcion))
            conn.commit()
            conn.close()
            return redirect(url_for('programas'))

    return render_template('agregar_programa.html')


@app.route('/programas/editar/<int:id>', methods=['GET', 'POST'])
def editar_programa(id):
    conn = sqlite3.connect('universidad.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        facultad = request.form['facultad']
        descripcion = request.form['descripcion']

        if nombre and facultad:
            cursor.execute('UPDATE programas SET nombre = ?, facultad = ?, descripcion = ? WHERE id = ?',
                           (nombre, facultad, descripcion, id))
            conn.commit()
            conn.close()
            return redirect(url_for('programas'))
    
 
    cursor.execute('SELECT * FROM programas WHERE id = ?', (id,))
    programa = cursor.fetchone()
    conn.close()
    
    if programa is None:
        return "Programa no encontrado", 404
        
    return render_template('editar_programa.html', programa=programa)

@app.route('/programas/eliminar/<int:id>')
def eliminar_programa(id):
    conn = sqlite3.connect('universidad.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM programas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('programas'))

if __name__ == '__main__':
    app.run(debug=True)