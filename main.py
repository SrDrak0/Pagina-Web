import os
import sqlite3
import google.generativeai as genai
import markdown

from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from flask_session import Session
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  
app.config['SECRET_KEY'] = 'Angel05g'
Session(app)

try:
  
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('models/gemini-pro-latest')
    print("✅ Modelo de IA configurado correctamente.")
except Exception as e:
    print(f"⚠️ Error al configurar el modelo de IA: {e}. Asegúrate de haber configurado la variable de entorno GOOGLE_API_KEY.")
    model = None



@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/mision")
def mision():
    return render_template('mision.html')

@app.route("/vision")
def vision():
    return render_template('vision.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        carrera = request.form['carrera']

        if not nombre or not apellido or not email or not carrera:
            error_msg = "Todos los campos son obligatorios. Por favor, inténtalo de nuevo."
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
            error_msg = "El correo electrónico ya está registrado. Utiliza otro."
            return render_template('registro.html', error=error_msg)

    return render_template('registro.html')

@app.route('/exito')
def exito():
    return render_template('exito.html')

@app.route("/programas")
def programas():
    conn = sqlite3.connect('universidad.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM programas ORDER BY facultad, nombre')
    lista_de_programas = cursor.fetchall()
    conn.close()
    return render_template('programas.html', programas=lista_de_programas)


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




@app.route('/ask_bot', methods=['POST'])
def ask_bot():
    if model is None:
        return jsonify({'error': 'El modelo de IA no está configurado correctamente.'}), 500

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({'error': 'Mensaje vacío.'}), 400

    if "chat_history" not in session:
        session["chat_history"] = [
            {
                "role": "user",
                "parts": ["Eres un asistente virtual amigable y servicial para la 'Universitaria de Colombia'. Tu objetivo es ayudar a los visitantes a encontrar información sobre la universidad, sus programas académicos, su misión, visión y cómo registrarse. Responde de forma concisa y útil."]
            },
            {
                "role": "model",
                "parts": ["¡Hola! Soy el asistente virtual de la Universitaria de Colombia. Pregúntame lo que necesites saber sobre nuestros programas, la misión de la universidad o cómo puedes registrarte."]
            }
        ]
    
    chat = model.start_chat(history=session["chat_history"])
    
    try:
        response = chat.send_message(user_message)
        session["chat_history"] = chat.history
        bot_response_html = markdown.markdown(response.text)
        
        return jsonify({'response': bot_response_html})

    except Exception as e:
        print(f"Error al llamar a la API de GenAI: {e}")
        return jsonify({'error': 'Hubo un problema al contactar al asistente.'}), 500




if __name__ == '__main__':
    app.run(debug=True)