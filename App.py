import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime #Nos permitirá darle el nombre a la foto

load_dotenv()
UPLOAD_FOLDER = os.path.join('static/images/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
# print(UPLOAD_FOLDER)

# MySQL Connection
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    data = cur.fetchall()
    return render_template('empleados/index.html', empleados = data)

@app.route('/create', methods=['POST'])
def agregar_empleado():
    if request.method == 'POST':
        _nombre = request.form['txtNombre']
        _correo = request.form['txtCorreo']
        if 'txtFoto' not in request.files:
            flash('Sin archivo')
            return redirect(request.url)
        _foto = request.files['txtFoto']
        if _foto.filename == '':
            flash('Ningún archivo seleccionado')
            return redirect(request.url)
        if _foto and allowed_file(_foto.filename):
            now = datetime.now()
            tiempo = now.strftime("%Y%H%M%S")
            filename = tiempo + secure_filename(_foto.filename)
            _foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s)', (_nombre, _correo, filename))
        mysql.connection.commit()
        flash('Empleado Agregado Correctamente')
    return redirect(url_for('index'))

"""
@app.route('/edit/<string:id>')
def obtener_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('empleados/edit.html', empleado = data[0])
"""

@app.route('/update/<string:id>', methods=['POST'])
def actualizar_empleado(id):
    if request.method == 'POST':
        _nombre = request.form['txtNombre']
        _correo = request.form['txtCorreo']
        if 'txtFoto' not in request.files:
            flash('Sin archivo')
            return redirect(request.url)
        _foto = request.files['txtFoto']
        if _foto.filename == '':
            flash('Ningún archivo seleccionado')
            return redirect(request.url)
        if _foto and allowed_file(_foto.filename):
            now = datetime.now()
            tiempo = now.strftime("%Y%H%M%S")
            filename = tiempo + secure_filename(_foto.filename)
            _foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
        cur = mysql.connection.cursor()
        cur.execute('SELECT foto FROM empleados WHERE id = %s', [id])
        fila = cur.fetchall()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fila[0][0]))
        cur.execute("""
            UPDATE empleados
            SET nombre = %s,
                correo = %s,
                foto = %s
            WHERE id = %s 
        """, (_nombre, _correo, filename, id))
        mysql.connection.commit()
        flash('Empleado Actualizado')
    return redirect(url_for('index'))

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['UPLOAD_FOLDER'], nombreFoto)

@app.route('/destroy/<string:id>')
def eliminar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT foto FROM empleados WHERE id = {0}'.format(id))
    fila = cur.fetchall()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fila[0][0]))
    cur.execute('DELETE FROM empleados WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Empleado Eliminado')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(
        host=os.getenv('DOMAIN'),
        port=os.getenv('PORT'),
        debug=os.getenv('DEBUG')
    )
 