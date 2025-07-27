from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

db_config = {
    'host': 'maestro1',
    'user': 'root',
    'password': 'root',
    'database': 'db_inventario'
}

def obtener_productos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, codigo, descripcion, unidad, categoria FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return productos

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    session.permanent = True
    username = request.form['username']
    password = request.form['password']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session['username'] = user['username']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', mensaje="Credenciales inválidas")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, codigo, descripcion, unidad, categoria FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('dashboard.html', productos=productos, username=session['username'])

@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    if 'username' not in session:
        return redirect(url_for('index'))

    nombre = request.form['nombre']
    codigo = request.form['codigo']
    descripcion = request.form['descripcion']
    unidad = request.form['unidad']
    categoria = request.form['categoria']

    if nombre == "" or codigo == "" or descripcion == "" or unidad == "" or categoria == "":
        productos = obtener_productos()
        return render_template('dashboard.html', productos=productos, mensaje="No se pudo enviar el formulario, campos incompletos", username=session['username'])

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM productos WHERE codigo = %s", (codigo,))
    existente = cursor.fetchone()

    if existente:
        cursor.close()
        conn.close()
        productos = obtener_productos()
        return render_template('dashboard.html', productos=productos, mensaje="Código de producto duplicado.", username=session['username'])

    cursor.execute("""
        INSERT INTO productos (nombre, codigo, descripcion, unidad, categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, codigo, descripcion, unidad, categoria))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    if 'username' not in session:
        return redirect(url_for('index'))

    codigo = request.form['codigo']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/editar_producto')
def editar_producto():
    if 'username' not in session:
        return redirect(url_for('index'))

    codigo = request.args.get('codigo')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, codigo, descripcion, unidad, categoria FROM productos WHERE codigo = %s", (codigo,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    # Traer todos los productos igual que el dashboard
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, codigo, descripcion, unidad, categoria FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('dashboard.html', producto=producto, productos=productos, username=session['username'])

@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    if 'username' not in session:
        return redirect(url_for('index'))

    nombre = request.form['nombre']
    codigo = request.form['codigo']
    descripcion = request.form['descripcion']
    unidad = request.form['unidad']
    categoria = request.form['categoria']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre = %s, descripcion = %s, unidad = %s, categoria = %s
        WHERE codigo = %s
    """, (nombre, descripcion, unidad, categoria, codigo))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)