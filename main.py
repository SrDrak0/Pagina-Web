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
    return render_template('programas.html')

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



if __name__ == '__main__':
    app.run(debug=True)