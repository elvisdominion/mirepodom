from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import supabase

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Ruta GET: Muestra el formulario de login
@admin_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# Ruta POST: Procesa el login
@admin_bp.route('/login', methods=['POST'])
def login_post():
    usuario = request.form['usuario']
    password = request.form['password']
    sede_id = request.form['sede']

    # Verificar credenciales
    resultado = supabase.table("usuarios").select("*").eq("usuario", usuario).eq("sede_id", sede_id).execute()

    if resultado.data:
        user = resultado.data[0]
        if user['password'] == password:
            session['usuario'] = usuario
            session['rol'] = user['rol']
            session['sede_id'] = int(sede_id)  # Almacenar la sede en la sesión
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for('personal.personal'))

    flash("Usuario, contraseña o sede incorrectos.", "danger")
    return redirect(url_for('admin.login'))


# Ruta para cerrar sesión
@admin_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Limpia la sesión
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('admin.login'))

